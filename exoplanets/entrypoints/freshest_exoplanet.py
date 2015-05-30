#!/usr/bin/env python
"""Prints terminal ASCII report of most recently updated
exoplanet system.
"""

from __future__ import absolute_import
from ..core import extract, formatters

def main():
    tree = extract.get_tree()
    most_recent = extract.most_recent_system(tree)
    print formatters.summarize_system(most_recent)
