#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261119 competition.

The front page is pre-rendered by render.py into entry.png next to this
file. This program only copies that image into the output directory
named by MAKEFUN_OUTPUT_DIR, so it runs with no network and produces
the same bytes on every run.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
