"""Entrypoint: render the Tuesday 24 November 2026 news image.

Writes one deterministic PNG to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png) and mirrors the same bytes to entry.png
next to this file for preview (best-effort: ignored on read-only
filesystems, e.g. the grader sandbox).
"""
import os
import shutil
import sys

# The grader runs `python3 -P -s main.py`: with -P the script's own
# directory is NOT on sys.path, so `import render` would fail.
# Insert it explicitly before importing the sibling module.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render

OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    img = render.build()
    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    try:
        shutil.copyfile(OUT, here)
    except OSError:
        # /bot is read-only in the grader sandbox; the mirror is only
        # a local preview, never let it fail the run.
        pass


if __name__ == "__main__":
    main()
