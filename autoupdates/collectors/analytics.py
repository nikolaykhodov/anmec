# -*- coding: utf-8 -*-

"""
Analytics collector
"""

from multiprocessing import Process, Queue, JoinableQueue
from collections import OrderedDict
from api import API
import argparse
import time
import os
import sys
import csv
import json


def parserWorker(ppid, task_queue, feed_queue, date_from, date_to, token=''):
    """ Parse groups and feed it to feed_queue """

    api = API(token)

    while not task_queue.empty():
        # Kill himself if parent is killed
        if os.getppid() != ppid:
            sys.exit()

        gid = task_queue.get()

        try:
            stat = api.stats.get(gid=gid, date_from=date_from, date_to=date_to)
            time.sleep(0.5)
        except Exception, ex:
            print str(ex)
            stat = {}
        finally:
            # Tell that the portion of groups is processed
            task_queue.task_done()

        entry = dict(
            gid=gid,
            stat=json.dumps(stat)
        )

        feed_queue.put(entry)

        time.sleep(0.4)


def feedWorker(ppid, feed_queue, outfile):
    """ Worker writes feed to file providing single point with atomic operations """

    fieldnames = OrderedDict([('gid', None), ('stat', None)])
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=",", quotechar='"')

    while 1:
        time.sleep(0.1)

        # If parent is killed, kill self, but before close file
        if os.getppid() != ppid:
            outfile.close()
            sys.exit()

        # Get line and write it down to file
        try:
            entry = feed_queue.get_nowait()
        except:
            continue

        if entry == '!!! STOP !!!':
            outfile.close()
            sys.exit()
        else:
            writer.writerow(entry)


def get_latest_line(f):
    """ Return how many lines are in file "f" """

    # Init vars
    lines = 0
    while f.readline() != '':
        lines += 1

    return lines


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


def test_tokens(tokens):
    print(" [x] Testing {0} tokens to be valid...".format(len(tokens)))
    good_tokens = []
    for token in tokens:
        if token == '':
            continue

        print(" [x] Testing token {0}...".format(token[:13] + '*****************' + token[:30]))
        api = API(token)
        try:
            response = api.execute(code='return "itworks";')
            print(response)
            if response == 'itworks':
                good_tokens.append(token)
        except:
            continue

    return good_tokens


def collect(gids_file, tokens_file, output, threads, date_from, date_to, progress_file=None):
    tokens = []
    feed_queue = Queue()
    task_queue = JoinableQueue()
    ppid = os.getpid()

    print " [x] Loading tokens..."
    for l in tokens_file:
        tokens.append(l.strip())

    tokens = test_tokens(tokens)

    if len(tokens) < threads:
        print(" [x] Error: not enough good tokens (number of tokens ({0}) < threads ({1}))".format(
            len(tokens),
            threads
        ))
        sys.exit()

    # Fill feed
    print " [x] Loading queue..."

    groups = []
    for l in gids_file:
        groups.append(l.strip())

    print " [x] ", len(groups), "groups in task..."

    last_line = get_latest_line(output)
    for gid in groups[last_line:]:
        task_queue.put(gid)

    print " [x] We skipped", last_line, " groups since they have been processed"

    print " [x] Loading completed."

    # Start processing
    print " [x] Start processing..."

    print " [x] Main PID = ", ppid

    # Start feed worker
    feed_worker = Process(target=feedWorker, args=(ppid, feed_queue, output))
    feed_worker.start()
    print " [x] Started feed worker (PID=", feed_worker.pid, ")"

    # Start the work that flushes the current progress a minute
    progress_worker = None
    if progress_file is not None:
        progress_worker = Process(target=progressWorker, args=(ppid, task_queue, progress_file.name))
        progress_worker.start()
        progress_file.close()
        print " [x] Start progress worker (PID=", progress_worker.pid, ")"

    # Start parsing workers
    workers = []
    for i in range(threads):
        p = Process(target=parserWorker, args=(ppid, task_queue, feed_queue, date_from, date_to, tokens[i], ))
        workers.append(p)
        p.start()

        print " [x] Started parsing worker (PID=", p.pid, ")"

    try:
        # Wait until all groups are processed
        for worker in workers:
            worker.join()

        # Send STOP message to feed worker
        feed_queue.put("!!! STOP !!!")

        # Wait until feed worker records all data to file
        feed_worker.join()
    finally:
        for worker in workers:
            worker.terminate()

        feed_worker.terminate()

        if progress_worker is not None:
            progress_worker.terminate()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gids-file', dest='gids_file',  help="txt file with one group id per line",
                        type=argparse.FileType('r'))
    parser.add_argument('-f', '--from', dest="date_from", help="date from [YYYY-MM-DD]")
    parser.add_argument('-t', '--to', dest='date_to', help="date to [YYYY-MM-DD]")
    parser.add_argument('-o', '--output', dest="output", help="output file", type=argparse.FileType('a+'))
    parser.add_argument('-p', '--progress-file', dest="progress_file", type=argparse.FileType('w+'))
    parser.add_argument('-T', '--threads', dest='threads', type=int, default=4)
    parser.add_argument('-a', '--access-tokens-file', dest="tokens_file", type=argparse.FileType('r'))
    parser.add_argument('action', choices=['collect'])
    args = parser.parse_args()

    if args.action == 'collect':
        collect(
            args.gids_file,
            args.tokens_file,
            args.output,
            args.threads,
            args.date_from,
            args.date_to,
            progress_file=args.progress_file
        )

if __name__ == '__main__':
    main()
