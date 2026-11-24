"""Entrypoint for the news-image-20261124 bounty entry.

The newspaper image for Tuesday 24 November 2026 is rendered offline
by render.py and committed to this repository as entry.png. At grade
time this program only copies those exact bytes into the output
directory: no rendering, no network, no clock, no randomness, and
standard library only — so the grader's minimal Python image can run
it without Pillow or system fonts.
"""

import hashlib
import os
import shutil
import sys


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        print(f"news-image-20261124: entry.png not found next to main.py ({source})", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)
    # Verify the copy: the bytes written to the output directory must
    # match the committed image exactly, otherwise fail loudly instead
    # of handing the grader a truncated or corrupted file.
    if _sha256(source) != _sha256(target):
        print("news-image-20261124: copied entry.png does not match the source image", file=sys.stderr)
        return 1
    print(f"news-image-20261124: copied entry.png to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
