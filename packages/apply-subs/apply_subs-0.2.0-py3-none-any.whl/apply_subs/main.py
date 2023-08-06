#!/usr/bin/env python3

import argparse
import json
import sys
import tempfile
from difflib import unified_diff
from pathlib import Path
from shutil import copy
from subprocess import CalledProcessError, run
from typing import List, Optional, Union

from colorama import Fore
from more_itertools import always_iterable
from schema import Or, Schema

from apply_subs import __version__

BASE_COMMAND = ["sed", "-i", "-e"]

SUBS_SCHEMA = Schema({str: Or(str, list)})


def _sub(to_replace: Union[str, List[str]], new: str, filename: str) -> str:
    for old in always_iterable(to_replace):
        comm = BASE_COMMAND + [f"s/{old}/{new}/g", filename]
        res = run(comm, capture_output=True, check=True)
    return res.stdout.decode()


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
    parser.add_argument("target", nargs="?", help="a target text file.")
    parser.add_argument(
        "subs",
        nargs="?",
        help="json file describing substitutions to apply (order matters).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--inplace", action="store_true")
    group.add_argument("-p", "--patch", action="store_true", help="print a patch.")
    group.add_argument(
        "-cp",
        "--cpatch",
        "--colored-patch",
        dest="colored_patch",
        action="store_true",
        help="print a colored patch.",
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

    if not Path(args.target).is_file():
        print(f"Error: {args.target} not found.", file=sys.stderr)
        return 1

    with open(args.subs, "r") as fh:
        subs = json.load(fh)

    if not SUBS_SCHEMA.is_valid(subs):
        print("Error: unrecognized json schema.", file=sys.stderr)
        return 1

    with tempfile.NamedTemporaryFile() as workfile:
        copy(args.target, workfile.name)
        for new, old in subs.items():
            try:
                _sub(old, new, workfile.name)
            except (CalledProcessError, FileNotFoundError):
                print(
                    f"Error: failed to apply subsitutions to {args.target}",
                    file=sys.stderr,
                )
                return 1
        with open(workfile.name, "r") as fh:
            new_content = fh.read()
    if args.inplace:
        with open(args.target, "w") as fh:
            fh.write(new_content)
    elif args.patch or args.colored_patch:
        s1 = open(args.target).read().splitlines(keepends=True)
        s2 = new_content.splitlines(keepends=True)
        diff = unified_diff(
            s1, s2, fromfile=args.target, tofile=f"{args.target} (patched)"
        )
        if args.colored_patch:
            diff = colored_diff(diff)
        print("".join(list(diff)))
    else:
        print(new_content, end="")
    return 0
