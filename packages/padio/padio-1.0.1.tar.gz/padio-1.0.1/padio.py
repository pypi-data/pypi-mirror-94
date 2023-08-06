#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import re
from pathlib import Path
from typing import Generator
from typing import List
from typing import Optional
from typing import Tuple


num_matcher = re.compile(r"([0-9]+)")


def extract_numbers(s: str) -> str:
    number_match = num_matcher.search(s)
    if number_match:
        return number_match.group(1)
    return ""


def calc_pad_length(files: List[Path]) -> int:
    max_len = 0
    for f in files:
        numbers = extract_numbers(f.name)
        max_len = max(len(numbers), max_len)
    return max_len


def parse_args(sys_args: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pads numbers in file names so they consistently align and sort"
    )
    parser.add_argument("files", nargs="+", metavar="file", help="Files to be renamed")
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        help="Length of numbers after padding (default: auto)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force rename, even if file at destination exists",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print all actions"
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Print actions only without modifying any file. Implies --verbose",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        metavar="REGEX",
        help="Regular expression used to ignore files matching the name",
    )
    parser.add_argument(
        "--ignore-files",
        nargs="+",
        metavar="IGNOREFILE",
        help="Files to ignore for renaming. Must add -- before positional arguments",
    )
    args = parser.parse_args(sys_args)

    # Dry run implies verbose
    if args.dry_run:
        args.verbose = True

    return args


def get_files(
    filenames: List[str],
    ignore_filenames: List[str],
    ignore_pattern: str,
) -> List[Path]:
    # Compile ignore pattern, if provided
    ignore_matcher: Optional[re.Pattern] = None
    if ignore_pattern:
        ignore_matcher = re.compile(ignore_pattern)

    p = Path(".")
    files: List[Path] = []
    for f in filenames:
        if ignore_filenames and f in ignore_filenames:
            continue
        if ignore_matcher and ignore_matcher.match(f):
            continue
        files.append(p / f)

    return files


def pad_files(
    files: List[Path],
    pad_len: int,
    verbose=False,
) -> Generator[Tuple[Path, Path], None, None]:
    for f in files:
        numbers = extract_numbers(f.name)
        if len(numbers) == pad_len:
            if verbose:
                print(f"{f.name} is already padded.")
            continue

        # Pad number and get destination path
        new_numbers = numbers.zfill(pad_len)
        new_name = num_matcher.sub(new_numbers, f.name, count=1)
        new_file = f.parent / new_name

        if f == new_file:
            if verbose:
                print(f"{f.name} already matches destination.")
            continue

        yield f, new_file


def main(sys_args: Optional[List[str]] = None) -> int:
    args = parse_args(sys_args)

    # Build list of files to act on
    files = get_files(args.files, args.ignore_files, args.ignore)

    pad_len = args.length
    if pad_len is None:
        pad_len = calc_pad_length(files)

    if args.verbose:
        print(f"Padding to {pad_len}")

    status = 0
    for f, new_file in pad_files(files, pad_len, args.verbose):
        # Possibly rename unless exists or forced
        if not new_file.exists() or args.force:
            if args.verbose:
                print(f"Rename {f.name} to {new_file.name}")
            if not args.dry_run:
                f.rename(new_file)
        else:
            print(
                f"Could not rename {f.name} to {new_file.name}. Destination file exists."
            )
            status = 1

    return status


if __name__ == "__main__":
    exit(main())
