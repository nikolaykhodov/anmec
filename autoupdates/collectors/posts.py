#!/usr/bin/env python
# -*- coding: utf8 -*-

from multiprocessing import Process, JoinableQueue
from collections import OrderedDict, namedtuple
from api import API
from datetime import datetime
from cStringIO import StringIO

import json
import argparse
import time
import os
import sys
import csv


Task = namedtuple('Task', ['gid', 'from_datetime'])


def timestamp2dt(timestamp):
    """ Convert UNIX timestamp to datetime object """

    return datetime.fromtimestamp(timestamp)


def parserWorker(ppid, delay, task_queue, feed_queue):
    """ Parse groups and feed it to feed_queue """

    api = API('')

    for task in iter(task_queue.get, 'STOP'):
        finished = False
        offset = 0
        post_count = -1

        try:
            while not finished:
                # Fetch API response
                wall = api.wall.get(count=100, owner_id='-' + task.gid, offset=offset)
                if post_count == -1:
                    post_count = wall[0]

                offset += 100
                last_post_date = timestamp2dt(wall[-1]['date'])
                finished = offset > post_count or last_post_date < task.from_datetime

                entries = []
                for post in wall[1:]:
                    date = datetime.fromtimestamp(int(post['date']))
                    timestamp = date.strftime('%Y-%m-%d %H:%M:%S +4:00')

                    entry = dict(
                        post_id="{0}_{1}".format(post['to_id'], post['id']),
                        date=timestamp,
                        likes=post.get('likes', {}).get('count', 0),
                        reposts=post.get('reposts', {}).get('count', 0),
                        comments=post.get('comments', {}).get('count', 0),
                        text=post['text'].encode('utf-8'),
                        attachments=json.dumps(post.get('attachments', {})).encode('utf-8')
                    )
                    entries.append(entry)
                feed_queue.put(entries)

                time.sleep(delay)

        except Exception as ex:
            print('Exception in parserWorker:', ex)
        finally:
            task_queue.task_done()

    print("parser worker finished")
    print("task_queue.qsize() = ", task_queue.qsize())


def progressWorker(ppid, task_queue, progress_filename):

    qsize = task_queue.qsize()

    while 1:
        time.sleep(1.0)

        # If parent is killed, kill self, but before close file
        if os.getppid() != ppid:
            sys.exit()

        progress_file = open(progress_filename, 'w+')
        progress_file.write("{0}/{1}".format(qsize - task_queue.qsize(), qsize))
        progress_file.close()

        if task_queue.qsize() == 0:
            sys.exit()


def flush_memory_outfile(memory_outfile, disk_outfile):
    memory_outfile.seek(0)
    content = memory_outfile.read()
    disk_outfile.write(content)
    memory_outfile.close()
    disk_outfile.flush()


def feedWorker(ppid, feed_queue, outfile):
    """ Worker writes feed to file providing single point with atomic operations """

    fields = [
        'post_id',
        'date',
        'likes',
        'reposts',
        'comments',
        'text',
        'attachments'
    ]
    fieldnames = OrderedDict([
        (field, None) for field in fields
    ])

    counter = 0
    memory_outfile = StringIO()
    writer = csv.DictWriter(memory_outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')

    for posts in iter(feed_queue.get, 'STOP'):

        try:
            for post in posts:
                writer.writerow(post)
        except Exception as ex:
            print('feedWorker: Exception =', ex)

        if memory_outfile.tell() > 10 ** 6:
            counter += 1
            print("Flushing...", counter)

            try:
                flush_memory_outfile(memory_outfile, outfile)
            finally:
                memory_outfile.close()
                memory_outfile = StringIO()
                writer = csv.DictWriter(memory_outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')

    outfile.close()


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


def collect(gids_file, output, threads, delay, from_datetime, progress_file=None):
    feed_queue = JoinableQueue()
    task_queue = JoinableQueue()
    ppid = os.getpid()

    # Fill feed
    print " [x] Loading queue..."

    for gid in gids_file:
        task_queue.put(Task(gid=gid.strip(), from_datetime=from_datetime))

    print " [x] Loading completed."

    # Start processing
    print " [x] Start processing..."
    print " [x] Main PID = ", ppid

    # Start feed worker
    feed_worker = Process(target=feedWorker, args=(ppid, feed_queue, output))
    feed_worker.start()
    print " [x] Started feed worker (PID=", feed_worker.pid, ")"

    progress_worker = None
    if progress_file is not None:
        progress_worker = Process(target=progressWorker, args=(ppid, task_queue, progress_file.name))
        progress_worker.start()
        progress_file.close()
        print " [x] Start progress worker (PID=", progress_worker.pid, ")"

    # Start parsing workers
    workers = []
    for i in range(threads):
        p = Process(target=parserWorker, args=(ppid, delay, task_queue, feed_queue))
        workers.append(p)
        p.start()
        print " [x] Started parsing worker (PID=", p.pid, ")"

    for index in range(len(workers)):
        task_queue.put('STOP')

    try:
        for worker in workers:
            worker.join()
        feed_queue.put('STOP')
    finally:
        for worker in workers:
            worker.terminate()

        if progress_worker is not None:
            progress_worker.terminate()


def mkdate(datestring):
    return datetime.strptime(datestring, '%Y-%m-%d')


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-g', '--gids-file', dest='gids_file',  help="txt file with one group id per line",
                        type=argparse.FileType('r'))
    parser.add_argument('-f', '--from-datetime', dest='from_datetime', type=mkdate)
    parser.add_argument('-o', '--output', dest='output', type=argparse.FileType('w+'))
    parser.add_argument('-p', '--progress-file', dest='progress_file', type=argparse.FileType('w+'))
    parser.add_argument('-c', '--collected_data', dest="collected_data", type=argparse.FileType('r'))
    parser.add_argument('-T', '--threads', dest='threads', type=int, default=4)
    parser.add_argument('-d', '--delay', dest='delay', type=float, default=0.1)
    parser.add_argument('action', choices=['collect'])
    args = parser.parse_args()

    arg_names = ['gids_file', 'from_datetime', 'output', 'progress_file', 'collected_data', 'threads', 'delay', 'action']
    for arg_name in arg_names:
        print(arg_name, '=', getattr(args, arg_name))

    if args.action == 'collect':
        collect(
            args.gids_file,
            args.output,
            args.threads,
            args.delay,
            args.from_datetime,
            progress_file=args.progress_file
        )


if __name__ == '__main__':
    main()
