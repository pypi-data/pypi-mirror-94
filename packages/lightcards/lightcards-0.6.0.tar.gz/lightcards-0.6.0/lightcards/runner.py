# Markdown flashcard utility
# Armaan Bhojwani 2021

import argparse
import curses
import os
import pkg_resources
from random import shuffle
import sys

from . import parse, progress
from .display import Display, CursesError
from .deck import Status


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Terminal flashcards from Markdown"
    )
    parser.add_argument(
        "-V",
        "--view",
        metavar="view",
        type=int,
        choices=range(1, 4),
        default=1,
        help="specify which view to start in (default = 1)",
    )
    parser.add_argument("inp", metavar="input file", type=str, nargs=1)
    parser.add_argument(
        "-a",
        "--alphabetize",
        action="store_true",
        help="alphabetize card order",
    )
    parser.add_argument(
        "-p",
        "--purge",
        action="store_true",
        help="don't check cached info before starting",
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="reverse card order"
    )
    parser.add_argument(
        "-s", "--shuffle", action="store_true", help="shuffle card order"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"lightcards {pkg_resources.require('lightcards')[0].version}",
    )
    return parser.parse_args()


def show(args, stack, headers, input_file):
    """
    Get objects from cache, manipulate deck according to passed arguments, and
    send it to the display functions
    """
    # Purge caches if asked
    if args.purge:
        progress.purge(get_orig()[1])

    # Check for caches
    idx = Status()
    cache = progress.dive(get_orig()[1])
    if cache:
        (stack) = cache

    # Manipulate deck
    if args.shuffle:
        shuffle(stack)
    if args.alphabetize:
        stack.sort(key=lambda x: x.front)
    if args.reverse:
        stack.reverse()

    # Send to display
    win = Display(stack, headers, idx, args.view, input_file)
    try:
        curses.wrapper(win.run)
    except curses.error as e:
        raise CursesError() from e


def get_orig():
    """Return original header and stack"""
    return (headers, stack)


def main(args=sys.argv):
    sys.tracebacklimit = 0
    args = parse_args()
    global headers, stack
    input_file = args.inp[0]
    (headers, stack) = parse.parse_html(parse.md2html(input_file))
    show(args, stack, headers, input_file)


if __name__ == "__main__":
    main()
