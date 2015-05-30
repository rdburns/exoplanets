#!/usr/bin/env python
"""Prints terminal ASCII report of most requested
exoplanet system.
"""

from __future__ import absolute_import

import sys
import argparse

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

    tree = extract.get_tree()

    if args.freshest:
        the_system = extract.most_recent_system(tree)
    else:
        the_system = extract.find_system_by_name(tree, args.system_name)
        if the_system is None:
            print "System not found."
            sys.exit(1)

    print formatters.summarize_system(the_system)
