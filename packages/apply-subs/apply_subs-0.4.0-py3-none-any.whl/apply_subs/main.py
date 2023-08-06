#!/usr/bin/env python3

import argparse
import json
import sys
from difflib import unified_diff
from pathlib import Path
from typing import List, Optional, Union

from colorama import Fore
from more_itertools import always_iterable
from schema import Or, Schema

from apply_subs import __version__

SUBS_SCHEMA = Schema({str: Or(str, list)})


def _sub(to_replace: Union[str, List[str]], new: str, content: str) -> str:
    for old in always_iterable(to_replace):
        content = content.replace(old, new)
    return content


def colored_diff(diff):
    # this is adapted from
    # https://chezsoi.org/lucas/blog/colored-diff-output-with-python.html

    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        else:
            yield line


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="*", help="target text file(s)")
    parser.add_argument(
        "-s",
        "--subs",
        action="store",
        help="json file describing substitutions to apply (order matters).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--inplace", action="store_true")
    group.add_argument("-d", "--diff", action="store_true", help="print a diff.")
    group.add_argument(
        "-cp",
        "--cdiff",
        "--colored-diff",
        dest="colored_diff",
        action="store_true",
        help="print a colored diff.",
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="print apply-subs version."
    )

    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    if argv is None:
        argv = sys.argv
        minlen = 3
    else:
        minlen = 2

    if len(argv) < minlen:
        parser.print_help(file=sys.stderr)
        return 1

    with open(args.subs, "r") as fh:
        subs = json.load(fh)

    if not SUBS_SCHEMA.is_valid(subs):
        print("Error: unrecognized json schema.", file=sys.stderr)
        return 1

    for target in args.target:
        if not Path(target).is_file():
            print(f"Error: {target} not found.", file=sys.stderr)
            return 1
        with open(target, "r") as fh:
            new_content = fh.read()

        for new, old in subs.items():
            new_content = _sub(old, new, new_content)

        if args.inplace:
            with open(target, "w") as fh:
                fh.write(new_content)
        elif args.diff or args.colored_diff:
            s1 = open(target).read().splitlines(keepends=True)
            s2 = new_content.splitlines(keepends=True)
            diff = unified_diff(s1, s2, fromfile=target, tofile=f"{target} (patched)")
            if args.colored_diff:
                diff = colored_diff(diff)
            print("".join(list(diff)))
        else:
            print(new_content, end="")
    return 0
