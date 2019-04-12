#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import os
from getopt import getopt, error
import time
import operator

params = {
    'source': '/opt/football',
    'destination': '/opt/by_dates',
    'sorted_dir': '/opt/sorted'
}

unix_options = "s:d:"
gnu_options = ["source=", "destination="]
keywords = ['футбол', 'чм']


def count_lines_in_file(path):
    with open(path, 'r') as f:
        count = sum(1 for line in f)
        f.close()
    return count


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def process_line(line):
    query, timestamp = line.strip().split('\t')
    d, t = timestamp.split(' ')
    uts = int(time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")))
    return query, timestamp, d, t, uts


def split_by_dates(src, output_dir):
    buffer = []
    prev = False
    with open(src, 'r') as fp:
        total = count_lines_in_file(src)
        for i, line in enumerate(fp):
            if i == 0:
                continue

            query, timestamp, rec_date, rec_time, uts = process_line(line)

            if rec_date != prev:
                with open('%s/%s.txt' % (output_dir, rec_date), 'a') as wp:
                    for item in buffer:
                        wp.write(item)
                print_progress_bar(i, total)
                buffer = []

            for word in query.split(' '):
                if word in keywords:
                    buffer.append(line)
                    break

            prev = rec_date


def make_top(src_dir, dst_dir):
    for filename in os.listdir(src_dir):
        path = "%s/%s" % (src_dir, filename)
        total = count_lines_in_file(path)
        output = {}
        with open(path, 'r') as fp:
            print("\nProcessing %s" % path)
            for i, line in enumerate(fp):
                query, date = line.strip().split(chr(9))
                if query in output:
                    output[query] += 1
                else:
                    output[query] = 1
            print_progress_bar(i, total)

        s = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
        with open("%s/%s-top.txt" % (dst_dir, filename), "w+") as wp:
            for line in s:
                wp.write('%s\t%s\n' % (line[1], line[0]))


try:
    if len(argv) > 1:
        arguments, values = getopt(argv[1:], unix_options, gnu_options)
        for argument, value in arguments:
            if argument in ("-i", "--input"):
                params['source'] = value
            elif argument in ("-o", "--output"):
                params['destination'] = value
    # split_by_dates(params['source'], params['destination'])
    make_top(params['destination'], params['sorted_dir'])
except error as err:
    print(str(err))
    exit(2)
