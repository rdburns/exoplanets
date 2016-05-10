#!/usr/bin/env python
"""Prints terminal ASCII report of most requested
exoplanet system.
"""

from __future__ import absolute_import

import os
import sys
import argparse
import time
from lxml import etree

from ..core import extract, formatters


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('system_name', nargs='*',
                        help=('All positional arguments are appended '
                              'to a string and used as a system name.')
                        )
    parser.add_argument('--freshest', action='store_true',
                        help=('Prints summary of most recently '
                        'updated system')
                        )
    args = parser.parse_args()

    # Join the positional args into a single string, so that
    # we can get spaces without requiring quotes around system names
    # on the command line
    full_name = ' '.join(args.system_name)
    args.system_name = full_name
    return args


def main():
    args = arguments()

    # Only download xml if older than:
    max_age = 60 * 60 * 12  # hours

    cache_fn = os.path.expanduser('~/exoplanets.xml')
    if os.path.isfile(cache_fn):
        st = os.stat(cache_fn)
        age = (time.time() - st.st_mtime)
    else:
        age = max_age + 1

    if age > max_age:
        print "Downloading database ..."
        tree = extract.get_tree()
        tree.write(cache_fn)
    else:
        print "Using cached database ..."
        tree = etree.parse(cache_fn)

    if args.freshest:
        the_system = extract.most_recent_system(tree)
    else:
        if args.system_name == '':
            for piped_input in sys.stdin:
                req_name = piped_input.rstrip()
        else:
            req_name = args.system_name
        the_system = extract.find_system_by_name(tree, req_name)
        if the_system is None:
            print "System not found."
            sys.exit(1)

    print formatters.summarize_system(the_system)
