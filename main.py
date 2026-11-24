#!/usr/bin/env python3
"""Entry point for the news-image-20261124 bounty entry.

The infographic is drawn offline by render.py and committed to this
repository as entry.png (a dense, newspaper-style summary of Tuesday
24 November 2026's world news). At grade time this program copies those
exact bytes to the output directory, so both harness runs write identical
output: no network, no clock, no randomness, standard library only.
"""

import os
import shutil
import sys


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    source_image = os.path.join(repo_root, "entry.png")
    # The grader mounts a writable /output; local checks point
    # MAKEFUN_OUTPUT_DIR at a scratch folder instead.
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    destination = os.path.join(output_dir, "entry.png")

    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source_image, destination)
    print(f"news-image-20261124: copied entry.png to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
