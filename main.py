"""Entrypoint: render the Tuesday 24 November 2026 news image.

Writes one deterministic PNG to /output/entry.png and mirrors the same
bytes to entry.png next to this file for preview.
"""
import os
import shutil

import render

OUT = "/output/entry.png"


def main():
    img = render.build()
    os.makedirs("/output", exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    shutil.copyfile(OUT, here)


if __name__ == "__main__":
    main()
