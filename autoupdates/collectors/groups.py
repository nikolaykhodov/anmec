#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Сборщик базы групп в ВК
mysql -u<user> -p --local-infile

LOAD DATA LOCAL INFILE './groups.txt' INTO TABLE groups COLUMNS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\n' (gid, type,members_count,is_closed,name,country,city);
"""
from multiprocessing import Process, Queue, JoinableQueue
from collections import OrderedDict
from api import API

import argparse
import time
import os
import sys
import csv


def parserWorker(ppid, task_queue, feed_queue, min_people=1000):
    """ Parse groups and feed it to feed_queue """

    api = API('')

    while not task_queue.empty():
        # Kill himself if parent is killed
        if os.getppid() != ppid:
            sys.exit()

        step = task_queue.get()

        # List of group numbers at this step
        gids = [str(i) for i in xrange(500 * (step - 1) + 1, 500 * step + 1)]

        # Fetch API response
        try:
            groups = api.groups.getById(gids=",".join(gids), fields="members_count,counters,place")
        except:
            continue
        finally:
            # Tell that the portion of groups is processed
            task_queue.task_done()

        # Save only groups and publc pages with number of participants greater
        # than @min_people
        type_map = {'group': 1, 'event': 2, 'page': 3}

        feed = ""
        feed = []
        for group in groups:
            try:
                members_count = int(group.get('members_count', 0))
                group_type = group.get('type', '')
                type_id = type_map.get(group_type, 4)  # 4 - unknown type

                if members_count < min_people:
                    continue

                group_name = group.get('name', '')[:300].encode('utf-8')
                group_name = group_name.replace('\n', '')

                # It will be supplied to feed_queue
                #feed = feed + u'%(gid)s,%(type)s,%(members_count)s,%(is_closed)s,"%(name)s",%(country)s,%(city)s\n' %
                entry = dict(
                    gid=group['gid'],
                    type=type_id,
                    members_count=members_count,
                    is_closed=group.get('is_closed', 1),
                    name=group_name,
                    country=group.get('place', {}).get('country', 0),
                    city=group.get('place', {}).get('city', 0)
                )

                feed.append(entry)
            except:
                continue

        feed_queue.put(feed)


def feedWorker(ppid, feed_queue, outfile):
    """ Worker writes feed to file providing single point with atomic operations """

    fieldnames = OrderedDict([('gid', None), ('type', None), ('members_count', None), ('is_closed', None), ('name', None), ('country', None), ('city', None)])
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')

    while 1:
        time.sleep(0.1)

        # If parent is killed, kill self, but before close file
        if os.getppid() != ppid:
            outfile.close()
            sys.exit()

        # Get line and write it down to file
        try:
            feed = feed_queue.get_nowait()
        except:
            continue

        if len(feed) == 1 and feed[0] == '!!! STOP !!!':
            outfile.close()
            sys.exit()
        else:
            for entry in feed:
                writer.writerow(entry)


def get_latest_gid(f):
    """ Return the latest process group """

    # Seek latest byte in order to enter the loop
    f.seek(-1, 2)

    # Init vars
    line = ''
    c = ''
    offset = 1

    while f.tell() > 0 and c != ',':
        f.seek(-offset, 2)
        c = f.read(1)
        offset += 1

    # Read character by character until "\n"
    while c != '\n' and f.tell() > 0:
        # Offset from the end of the file
        f.seek(-offset, 2)

        # Read one characte and prepend line
        c = f.read(1)
        line = c + line
        offset += 1

    line = line.strip().split(',')

    # Remove quote char
    return line[0].replace('"', '')


def get_groups_count():
    # 10-05-2013 7.51pm
    return 53543615


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from', dest='from_gid', type=int)
    parser.add_argument('-t', '--to', dest='to_gid', type=int)
    parser.add_argument('-o', '--output', dest='output', type=argparse.FileType('a+'))
    parser.add_argument('-c', '--collected_data', dest="collected_data", type=argparse.FileType('r'))
    parser.add_argument('-T', '--thread', dest='threads', type=int, default=4)
    parser.add_argument('-m', '--min-people', dest='min_people', type=int, default=1000)
    parser.add_argument('action', choices=['collect', 'last_gid', 'groups_count'])
    args = parser.parse_args()

    if args.action == 'last_gid':
        print get_latest_gid(args.collected_data)
    elif args.action == 'groups_count':
        print get_groups_count()
    elif args.action == 'collect':
        # Compute feed
        from_gid = args.from_gid
        to_gid = args.to_gid

        feed_queue = Queue()
        task_queue = JoinableQueue()
        ppid = os.getpid()

        # Fill feed
        print " [x] Loading queue..."

        for offset in xrange(from_gid / 500 + 1, to_gid / 500 + 2):
            task_queue.put(offset)

        print " [x] Loading completed."

        # Start processing
        print " [x] Start processing..."

        print " [x] Main PID = ", ppid

        # Start feed worker
        feed_worker = Process(target=feedWorker, args=(ppid, feed_queue, args.output))
        feed_worker.start()
        print " [x] Started feed worker (PID=", feed_worker.pid, ")"

        # Start parsing workers
        workers = []
        for i in range(args.threads):
            p = Process(target=parserWorker, args=(ppid, task_queue, feed_queue, args.min_people))
            workers.append(p)
            p.start()
            print " [x] Started parsing worker (PID=", p.pid, ")"

        try:
            # Wait until all groups are processed
            for worker in workers:
                worker.join()

            # Send STOP message to feed worker
            feed_queue.put(["!!! STOP !!!"])

            # Wait until feed worker records all data to file
            feed_worker.join()
        finally:
            for worker in workers:
                worker.terminate()

            feed_worker.terminate()

if __name__ == '__main__':
    main()
