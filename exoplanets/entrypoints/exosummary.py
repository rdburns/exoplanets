#!/usr/bin/env python
"""Prints terminal ASCII report of most requested
exoplanet system.
"""

from __future__ import absolute_import

from ..core import extract, formatters

import argparse


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('system_name', nargs='*',
                        help=('All positional arguments are appended '
                              'to a string and used as a system name.')
                        )
    args = parser.parse_args()

    # Join the positional args into a single string, so that
    # we can get spaces without requiring quotes around system names
    # on the command line
    full_name = ''.join(args.system_name)
    args.system_name = full_name
    return args


def main():
    args = arguments()
    print args.system_name
    tree = extract.get_tree()


    most_recent = extract.most_recent_system(tree)
    print formatters.summarize_system(most_recent)
