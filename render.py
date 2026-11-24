#!/usr/bin/env python3
"""Render the news-image-20261124 entry: one dense newspaper-style image
summing up the world news of Tuesday 24 November 2026.

Run locally (Pillow):  python3 render.py
Writes entry.png next to this file. The make.fun program (main.py) only
copies those bytes to the output directory, so the graded runs are
byte-identical and need nothing beyond the standard library.

Every story drawn here happened, or was first reported, on Tuesday
24 November 2026 in some time zone. Sources were read on 24 Nov 2026
(WIB): The Hindu BusinessLine, Reuters, Times of India, Jagran Josh,
AP, The Guardian, PANA, TradingView. Original drawings only.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
M = 16  # page margin

CREAM = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 53, 43)
GRAY = (90, 90, 90)
RULE = (60, 60, 60)
SEA = (168, 200, 224)
SAND = (232, 214, 176)
LAND = (196, 205, 170)

REGION = {
    "EUROPE": (43, 108, 176),
    "MIDDLE EAST": (179, 53, 43),
    "ASIA": (221, 107, 32),
    "AMERICAS": (47, 133, 90),
    "AFRICA": (107, 70, 193),
    "OCEANIA": (44, 122, 123),
    "GLOBAL": (74, 85, 104),
    "SPORT": (39, 103, 73),
    "TECH": (85, 60, 140),
    "BUSINESS": (120, 90, 20),
    "CULTURE": (160, 60, 110),
    "HEALTH": (180, 80, 80),
    "MARKETS": (120, 90, 20),
}

FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    for base in (FD, FL):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
COND_B = lambda s: font("LiberationSans-Bold.ttf", s)
COND = lambda s: font("LiberationSans-Regular.ttf", s)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=99):
    if leading is None:
        leading = int(fnt.size * 1.18)
    lines = wrap(d, text, fnt, max_w)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def chip(d, x, y, label, fill):
    f = SANS_B(8)
    w = int(d.textlength(label, font=f)) + 8
    d.rounded_rectangle([x, y, x + w, y + 13], 3, outline=fill, width=1)
    d.text((x + 4, y + 2), label, font=f, fill=fill)
    return x + w


def num_badge(d, x, y, n, color):
    d.ellipse([x, y, x + 15, y + 15], fill=color)
    f = SANS_B(9)
    s = str(n)
    tw = d.textlength(s, font=f)
    d.text((x + (15 - tw) / 2, y + 2), s, font=f, fill=(255, 255, 255))
    return x + 19


def flag_india(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(246, 137, 32))
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(19, 136, 8))
    d.ellipse([x + w / 2 - 3, y + h / 2 - 3, x + w / 2 + 3, y + h / 2 + 3],
              outline=(0, 0, 128), width=1)
    d.rectangle([x, y, x + w, y + h], outline=(120, 120, 120), width=1)


def flag_nepal(d, x, y, w, h):
    d.polygon([(x, y), (x + w, y + h * 0.28), (x + w * 0.45, y + h * 0.28),
               (x + w, y + h * 0.62), (x, y + h)], fill=(220, 20, 60),
              outline=(0, 56, 147))
    d.ellipse([x + 4, y + 3, x + 10, y + 9], fill=(255, 255, 255))


def flag_pl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 2], fill=(255, 255, 255))
    d.rectangle([x, y + h / 2, x + w, y + h], fill=(220, 20, 60))
    d.rectangle([x, y, x + w, y + h], outline=(150, 150, 150), width=1)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    star(d, x + 8, y + 7, 4, (255, 222, 0))


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def ship(d, x, y, w, hull=(40, 40, 48)):
    d.polygon([(x, y), (x + w, y), (x + w * 0.88, y + 9), (x + w * 0.1, y + 9)],
              fill=hull)
    d.rectangle([x + w * 0.12, y - 7, x + w * 0.8, y], fill=(180, 60, 40))
    d.rectangle([x + w * 0.8, y - 13, x + w * 0.92, y], fill=(230, 230, 230))


def flame(d, cx, cy, s):
    d.polygon([(cx, cy - s), (cx + s * 0.55, cy + s * 0.2), (cx + s * 0.3, cy + s),
               (cx - s * 0.3, cy + s), (cx - s * 0.55, cy + s * 0.2)],
              fill=(240, 120, 30))
    d.polygon([(cx, cy - s * 0.4), (cx + s * 0.3, cy + s * 0.35),
               (cx - s * 0.3, cy + s * 0.35)], fill=(250, 200, 60))


def drone(d, cx, cy, s=1.0):
    d.rectangle([cx - 12 * s, cy - 2 * s, cx + 12 * s, cy + 2 * s],
                fill=(50, 50, 55))
    d.ellipse([cx - 17 * s, cy - 7 * s, cx - 8 * s, cy - 3 * s],
              outline=(50, 50, 55), width=1)
    d.ellipse([cx + 8 * s, cy - 7 * s, cx + 17 * s, cy - 3 * s],
              outline=(50, 50, 55), width=1)
    d.rectangle([cx - 3 * s, cy - 5 * s, cx + 3 * s, cy + 5 * s],
                fill=(50, 50, 55))


# ---------------------------------------------------------------- illustrations

def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 246, 238))
    # draft document with the missing words boxed
    dx, dy = x + w * 0.14, y + 8
    d.rectangle([dx, dy, dx + w * 0.46, dy + h - 22], fill=(255, 255, 255),
                outline=(160, 160, 160), width=1)
    for i in range(5):
        ly = dy + 8 + i * 11
        d.line([dx + 6, ly, dx + w * 0.46 - 8, ly], fill=(190, 190, 190), width=2)
    d.rectangle([dx + 6, dy + 30, dx + w * 0.34, dy + 39], fill=(255, 255, 255),
                outline=RED, width=1)
    d.text((dx + 8, dy + 31), "fossil fuels?", font=SANS_B(8), fill=RED)
    # big red X over the document: no deal
    d.line([dx, dy, dx + w * 0.46, dy + h - 22], fill=RED, width=3)
    d.line([dx + w * 0.46, dy, dx, dy + h - 22], fill=RED, width=3)
    # thermometer
    tx = x + w * 0.8
    d.rounded_rectangle([tx - 5, y + 8, tx + 5, y + h - 28], 5,
                        outline=(120, 120, 120), width=1, fill=(255, 255, 255))
    d.rectangle([tx - 3, y + h * 0.35, tx + 3, y + h - 28], fill=RED)
    d.ellipse([tx - 9, y + h - 32, tx + 9, y + h - 14], fill=RED)
    d.text((x + w * 0.58, y + h - 13), "COP31 · ANTALYA", font=SANS_B(8),
           fill=GRAY)


def ill_warship(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # port quay
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(150, 140, 120))
    # corvette
    sx, sy = x + w * 0.18, y + h * 0.62
    d.polygon([(sx, sy), (sx + w * 0.62, sy), (sx + w * 0.55, sy + 12),
               (sx + w * 0.08, sy + 12)], fill=(70, 80, 95))
    d.rectangle([sx + w * 0.2, sy - 12, sx + w * 0.42, sy], fill=(95, 105, 120))
    d.rectangle([sx + w * 0.46, sy - 18, sx + w * 0.5, sy], fill=(60, 70, 85))
    # damage: fire + smoke
    flame(d, sx + w * 0.3, sy - 16, 11)
    for i in range(3):
        d.ellipse([sx + w * 0.26 + i * 4, sy - 30 - i * 6,
                   sx + w * 0.4 + i * 4, sy - 18 - i * 6], fill=(105, 105, 105))
    # sea drones closing in
    for fx in (0.06, 0.88):
        dx = x + w * fx
        d.polygon([(dx, y + h * 0.8), (dx + 16, y + h * 0.8),
                   (dx + 13, y + h * 0.86), (dx + 3, y + h * 0.86)],
                  fill=(40, 40, 48))
        d.line([dx + 8, y + h * 0.8, dx + 8, y + h * 0.74], fill=(40, 40, 48),
               width=2)
    d.text((x + 6, y + 4), "BENGHAZI NAVAL BASE", font=SANS_B(8), fill=INK)
    d.text((x + 6, y + h - 12), "LIBYA", font=SANS_B(8), fill=(255, 255, 255))


def ill_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.polygon([(x, y), (x + w * 0.42, y), (x + w * 0.3, y + h * 0.55),
               (x, y + h * 0.62)], fill=SAND)          # Arabia side
    d.polygon([(x + w, y), (x + w * 0.62, y), (x + w * 0.74, y + h * 0.5),
               (x + w, y + h * 0.45)], fill=(214, 190, 150))  # Iran side
    ship(d, x + w * 0.34, y + h * 0.68, w * 0.36)
    flame(d, x + w * 0.52, y + h * 0.56, 9)
    # missile arc + intercept star
    d.arc([x + w * 0.5, y + h * 0.04, x + w * 0.98, y + h * 0.6], 200, 320,
          fill=RED, width=2)
    star(d, x + w * 0.58, y + h * 0.28, 10, (250, 190, 40))
    d.text((x + 6, y + 4), "IRAN", font=SANS_B(9), fill=INK)
    d.text((x + 6, y + h - 15), "SAUDI ARABIA", font=SANS_B(9), fill=INK)
    d.text((x + w * 0.38, y + h * 0.88), "STRAIT OF HORMUZ", font=SANS_B(8),
           fill=(255, 255, 255))


def ill_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    # courthouse: pediment + entablature + columns
    cx = x + w / 2
    d.polygon([(x + w * 0.1, y + h * 0.28), (cx, y + 6), (x + w * 0.9, y + h * 0.28)],
              fill=(120, 110, 95))
    d.rectangle([x + w * 0.1, y + h * 0.28, x + w * 0.9, y + h * 0.35],
                fill=(105, 95, 80))
    for i in range(6):
        colx = x + w * 0.15 + i * w * 0.13
        d.rectangle([colx, y + h * 0.37, colx + 6, y + h - 18],
                    fill=(175, 165, 145))
    d.rectangle([x + w * 0.1, y + h - 18, x + w * 0.9, y + h - 11],
                fill=(105, 95, 80))
    # scales of justice, drawn in front of the columns
    sx = cx
    top = y + h * 0.42
    d.line([sx, top, sx, y + h - 24], fill=(90, 70, 30), width=2)
    d.line([sx - 17, top + 4, sx + 17, top + 4], fill=(90, 70, 30), width=2)
    for px in (sx - 17, sx + 17):
        d.line([px, top + 4, px - 6, top + 14], fill=(90, 70, 30), width=1)
        d.line([px, top + 4, px + 6, top + 14], fill=(90, 70, 30), width=1)
        d.arc([px - 7, top + 10, px + 7, top + 22], 0, 180,
              fill=(90, 70, 30), width=2)
    d.text((x + w * 0.32, y + h - 13), "THE HAGUE · ICJ", font=SANS_B(8),
           fill=GRAY)


def ill_nvidia(d, x, y, w, h):
    # chipmaker's boardroom return: a chip on a rising market chart
    d.rectangle([x, y, x + w, y + h], fill=(22, 32, 24))
    pts = [(x + 8, y + h - 22), (x + w * 0.3, y + h - 34),
           (x + w * 0.45, y + h - 28), (x + w * 0.65, y + h - 52),
           (x + w * 0.85, y + h - 62), (x + w - 8, y + h - 78)]
    d.line(pts, fill=(118, 185, 0), width=3)
    d.polygon([(x + w - 26, y + h - 78), (x + w - 8, y + h - 78),
               (x + w - 8, y + h - 62)], fill=(118, 185, 0))
    cx, cy = x + w * 0.24, y + h * 0.30
    d.rectangle([cx - 26, cy - 16, cx + 26, cy + 16], fill=(40, 40, 48),
                outline=(118, 185, 0), width=2)
    for px in (-18, 0, 18):
        d.line([cx + px, cy - 16, cx + px, cy - 24], fill=(118, 185, 0), width=2)
        d.line([cx + px, cy + 16, cx + px, cy + 24], fill=(118, 185, 0), width=2)
    d.text((cx - 13, cy - 7), "NVDA", font=SANS_B(10), fill=(118, 185, 0))
    d.text((x + w * 0.58, y + 8), "+31%", font=SERIF_B(22), fill=(255, 255, 255))
    d.text((x + 6, y + h - 13), "SANTA CLARA · CHIPMAKER", font=SANS_B(7),
           fill=(200, 200, 200))


def ill_train(d, x, y, w, h):
    # the Saryu-Kamala Express crossing a river bridge, Ayodhya to Janakpur
    d.rectangle([x, y, x + w, y + h], fill=(222, 234, 240))
    d.ellipse([x + w * 0.72, y + 8, x + w * 0.86, y + 22], fill=(245, 220, 130))
    d.polygon([(x, y + h * 0.55), (x + w, y + h * 0.55), (x + w, y + h),
               (x, y + h)], fill=(140, 170, 190))
    d.rectangle([x, y + h * 0.62, x + w, y + h * 0.68], fill=(90, 90, 90))
    # locomotive + two coaches
    lx = x + w * 0.10
    d.rectangle([lx, y + h * 0.34, lx + w * 0.34, y + h * 0.62],
                fill=(179, 53, 43))
    d.rectangle([lx + w * 0.36, y + h * 0.38, lx + w * 0.60, y + h * 0.62],
                fill=(30, 80, 130))
    d.rectangle([lx + w * 0.62, y + h * 0.38, lx + w * 0.86, y + h * 0.62],
                fill=(240, 200, 60))
    for wx in (0.05, 0.15, 0.25):
        d.rectangle([lx + w * wx, y + h * 0.42, lx + w * (wx + 0.07),
                     y + h * 0.52], fill=(220, 235, 245))
    d.ellipse([lx + w * 0.05, y + h * 0.62, lx + w * 0.12, y + h * 0.70],
              fill=(30, 30, 30))
    d.ellipse([lx + w * 0.42, y + h * 0.62, lx + w * 0.49, y + h * 0.70],
              fill=(30, 30, 30))
    d.ellipse([lx + w * 0.70, y + h * 0.62, lx + w * 0.77, y + h * 0.70],
              fill=(30, 30, 30))
    d.text((x + 6, y + h - 13), "AYODHYA – JANAKPUR", font=SANS_B(7), fill=INK)


def ill_kyiv_hit(d, x, y, w, h):
    # a residential block hit overnight: smoke, broken windows, searchlight
    d.rectangle([x, y, x + w, y + h], fill=(38, 42, 52))
    bx, by = x + w * 0.22, y + h * 0.30
    d.rectangle([bx, by, bx + w * 0.56, y + h - 8], fill=(120, 112, 104))
    for r in range(4):
        for c in range(5):
            wx = bx + 8 + c * (w * 0.56 - 14) / 5
            wy = by + 8 + r * (h * 0.58) / 4
            fill = (20, 20, 24) if (r * 5 + c) % 4 == 0 else (245, 220, 130)
            d.rectangle([wx, wy, wx + 9, wy + 10], fill=fill)
    d.polygon([(bx + w * 0.28, by), (bx + w * 0.56, by),
               (bx + w * 0.56, by + 16), (bx + w * 0.40, by + 10)],
              fill=(70, 66, 60))
    for i in range(3):
        d.ellipse([bx + w * 0.30 + i * 4, by - 10 - i * 7,
                   bx + w * 0.42 + i * 4, by - 1 - i * 7], fill=(140, 140, 140))
    d.polygon([(x + w * 0.86, y + h - 8), (x + w * 0.62, y + h * 0.30),
               (x + w * 0.98, y + h * 0.30)], fill=(245, 235, 180))
    d.text((x + 6, y + 4), "DYMER · KYIV REGION", font=SANS_B(7),
           fill=(255, 255, 255))


def ill_factory_blaze(d, x, y, w, h):
    # the candy factory in Cikande, Banten, burning through the night
    d.rectangle([x, y, x + w, y + h], fill=(30, 28, 34))
    bx, by = x + w * 0.12, y + h * 0.42
    d.rectangle([bx, by, bx + w * 0.76, y + h - 6], fill=(90, 84, 78))
    for c in range(6):
        wx = bx + 8 + c * (w * 0.76 - 14) / 6
        d.rectangle([wx, by + 8, wx + 10, by + 26], fill=(245, 180, 60))
    flame(d, bx + w * 0.20, by - 6, 1.2)
    flame(d, bx + w * 0.55, by - 10, 1.5)
    flame(d, bx + w * 0.78, by - 4, 1.0)
    d.ellipse([bx + w * 0.30, by - 26, bx + w * 0.45, by - 12],
              fill=(120, 120, 120))
    d.ellipse([bx + w * 0.55, by - 34, bx + w * 0.72, by - 18],
              fill=(100, 100, 100))
    d.text((x + 6, y + h - 13), "CIKANDE · BANTEN", font=SANS_B(7),
           fill=(255, 255, 255))


def icon_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 214, 228))
    bx, by = x + w * 0.18, y + h * 0.32
    d.rectangle([bx, by, bx + w * 0.55, y + h - 6], fill=(150, 140, 130))
    for r in range(3):
        for c in range(4):
            wx = bx + 7 + c * (w * 0.55 - 12) / 4
            wy = by + 6 + r * (h * 0.6) / 3
            fill = (70, 70, 80) if (r + c) % 3 else (240, 220, 150)
            d.rectangle([wx, wy, wx + 8, wy + 10], fill=fill)
    d.polygon([(bx + w * 0.38, by), (bx + w * 0.55, by), (bx + w * 0.55, by + 14),
               (bx + w * 0.45, by + 8)], fill=(80, 75, 70))
    for i in range(3):
        d.ellipse([bx + w * 0.4 + i * 3, by - 7 - i * 6,
                   bx + w * 0.5 + i * 3, by + 1 - i * 6], fill=(110, 110, 110))
    drone(d, x + w * 0.84, y + h * 0.22, 0.8)
    d.text((x + 5, y + 3), "KYIV REGION", font=SANS_B(7), fill=INK)


def icon_nepal_india(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    flag_nepal(d, x + w * 0.14, y + 8, 38, 28)
    flag_india(d, x + w * 0.6, y + 8, 42, 28)
    d.line([x + w * 0.14 + 19, y + 36, x + w * 0.14 + 19, y + h - 18],
           fill=(100, 80, 60), width=3)
    d.line([x + w * 0.6 + 21, y + 36, x + w * 0.6 + 21, y + h - 18],
           fill=(100, 80, 60), width=3)
    # plane arriving
    d.polygon([(x + w * 0.36, y + h * 0.62), (x + w * 0.58, y + h * 0.56),
               (x + w * 0.52, y + h * 0.7), (x + w * 0.42, y + h * 0.72)],
              fill=(70, 90, 140))
    d.text((x + w * 0.26, y + h - 12), "NEW DELHI", font=SANS_B(7), fill=GRAY)


def icon_factory_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 55, 60))
    d.rectangle([x + 8, y + h * 0.48, x + w - 8, y + h - 5], fill=(90, 85, 90))
    for i in range(4):
        d.rectangle([x + 14 + i * (w - 34) / 4, y + h * 0.58,
                     x + 23 + i * (w - 34) / 4, y + h * 0.78], fill=(250, 180, 60))
    flame(d, x + w * 0.34, y + h * 0.34, 12)
    flame(d, x + w * 0.6, y + h * 0.3, 15)
    d.text((x + 5, y + 3), "CANDY FACTORY FIRE", font=SANS_B(7),
           fill=(255, 255, 255))


def icon_westbank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 195))
    # village houses
    for i, fx in enumerate((0.08, 0.38, 0.66)):
        hx = x + w * fx
        d.rectangle([hx, y + h * 0.5, hx + w * 0.24, y + h - 8],
                    fill=(200, 185, 160))
        d.polygon([(hx - 2, y + h * 0.5), (hx + w * 0.12, y + h * 0.36),
                   (hx + w * 0.26, y + h * 0.5)], fill=(150, 90, 60))
    # burning car
    cx = x + w * 0.42
    d.rectangle([cx, y + h * 0.78, cx + w * 0.3, y + h * 0.88], fill=(60, 60, 70))
    d.rectangle([cx + 6, y + h * 0.7, cx + w * 0.22, y + h * 0.78],
                fill=(60, 60, 70))
    flame(d, cx + w * 0.15, y + h * 0.62, 10)
    d.text((x + 5, y + 3), "WEST BANK VILLAGES", font=SANS_B(7), fill=INK)


def icon_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 180, 110))
    d.rectangle([x + w * 0.42, y + 5, x + w * 0.58, y + h - 5], fill=(220, 200, 160))
    for sx in (x + w * 0.46, x + w * 0.5, x + w * 0.54):
        d.line([sx, y + 9, sx, y + 18], fill=(250, 230, 120), width=2)
    d.ellipse([x + w * 0.66, y + h * 0.5, x + w * 0.66 + 9, y + h * 0.5 + 9],
              fill=(200, 40, 40))
    d.text((x + 5, y + 3), "720/9d", font=SANS_B(11), fill=(255, 255, 255))
    d.text((x + 5, y + h - 11), "WELLINGTON", font=SANS_B(7), fill=(255, 255, 255))


def icon_football(d, x, y, w, h, score="4-0"):
    d.rectangle([x, y, x + w, y + h], fill=(90, 160, 90))
    d.rectangle([x + 7, y + 5, x + w - 7, y + h - 5], outline=(255, 255, 255),
                width=2)
    d.line([x + w / 2, y + 5, x + w / 2, y + h - 5], fill=(255, 255, 255), width=2)
    d.ellipse([x + w / 2 - 10, y + h / 2 - 10, x + w / 2 + 10, y + h / 2 + 10],
              outline=(255, 255, 255), width=2)
    d.ellipse([x + w / 2 - 4, y + h / 2 - 4, x + w / 2 + 4, y + h / 2 + 4],
              fill=(255, 255, 255), outline=(60, 60, 60), width=1)
    d.text((x + 5, y + h - 13), score, font=SANS_B(10), fill=(255, 255, 255))


def icon_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # capsizing boat: tilted hull
    cx, cy = x + w * 0.5, y + h * 0.55
    d.polygon([(cx - w * 0.34, cy + 6), (cx + w * 0.3, cy - 8),
               (cx + w * 0.36, cy + 2), (cx - w * 0.2, cy + 14)],
              fill=(120, 80, 50))
    d.line([cx - 2, cy - 2, cx + 8, cy - 20], fill=(90, 60, 40), width=3)
    # waves
    for i in range(4):
        wx = x + 8 + i * (w - 20) / 4
        d.arc([wx, y + h * 0.72, wx + 18, y + h * 0.86], 180, 360,
              fill=(255, 255, 255), width=2)
    d.text((x + 5, y + 3), "NIGERIA", font=SANS_B(7), fill=INK)


def icon_missiles_pl(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(215, 228, 240))
    flag_pl(d, x + 6, y + 6, 34, 22)
    # missile arcs coming down
    for fx in (0.55, 0.78):
        mx = x + w * fx
        d.arc([mx - 26, y + 4, mx + 10, y + h * 0.75], 300, 80, fill=RED, width=2)
        star(d, mx + 8, y + h * 0.68, 7, (250, 190, 40))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(170, 185, 150))
    d.text((x + 5, y + h - 19), "POLAND", font=SANS_B(7), fill=INK)


def icon_border_talks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 228))
    flag_india(d, x + 6, y + h * 0.3, 32, 21)
    flag_cn(d, x + w - 38, y + h * 0.3, 32, 21)
    # mountain frontier line between
    d.polygon([(x + w * 0.34, y + h * 0.72), (x + w * 0.5, y + h * 0.34),
               (x + w * 0.66, y + h * 0.72)], fill=(160, 170, 160))
    d.polygon([(x + w * 0.46, y + h * 0.44), (x + w * 0.5, y + h * 0.34),
               (x + w * 0.54, y + h * 0.44)], fill=(255, 255, 255))
    d.text((x + w * 0.3, y + 4), "ARUNACHAL TALKS", font=SANS_B(7), fill=GRAY)


def icon_castle(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 245))
    cx = x + w / 2
    # tiered castle roof (Shuri style, vermilion)
    d.polygon([(cx - w * 0.34, y + h * 0.42), (cx, y + h * 0.14),
               (cx + w * 0.34, y + h * 0.42)], fill=(180, 50, 40))
    d.polygon([(cx - w * 0.26, y + h * 0.6), (cx, y + h * 0.4),
               (cx + w * 0.26, y + h * 0.6)], fill=(195, 60, 45))
    d.rectangle([cx - w * 0.2, y + h * 0.6, cx + w * 0.2, y + h - 8],
                fill=(245, 240, 230))
    d.rectangle([cx - 5, y + h * 0.7, cx + 5, y + h - 8], fill=(120, 60, 40))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(170, 185, 150))
    d.text((x + 5, y + 3), "SHURI CASTLE, OKINAWA", font=SANS_B(6), fill=INK)


def icon_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(35, 40, 60))
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - 15, cy - 12, cx + 15, cy + 12], fill=(70, 160, 220),
                outline=(200, 230, 255), width=1)
    d.text((cx - 8, cy - 5), "AI", font=SANS_B(11), fill=(255, 255, 255))
    for i in range(-2, 3):
        d.line([cx + i * 6, cy - 12, cx + i * 6, cy - 19], fill=(200, 230, 255),
               width=2)
        d.line([cx + i * 6, cy + 12, cx + i * 6, cy + 19], fill=(200, 230, 255),
               width=2)
    d.text((x + 5, y + h - 11), "NVIDIA · CHINA", font=SANS_B(7),
           fill=(200, 230, 255))


def icon_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 238, 228))
    d.line([x + 8, y + h - 10, x + w - 8, y + h - 10], fill=INK, width=2)
    d.line([x + 8, y + 8, x + 8, y + h - 10], fill=INK, width=2)
    bars = [(0.20, 0.30), (0.38, 0.45), (0.56, 0.62), (0.74, 0.85)]
    for fx, fh in bars:
        bx = x + w * fx
        d.rectangle([bx, y + h - 10 - h * fh, bx + w * 0.12, y + h - 10],
                    fill=(47, 133, 90))
    d.line([(x + w * 0.14, y + h * 0.62), (x + w * 0.86, y + h * 0.16)],
           fill=(179, 53, 43), width=2)
    d.text((x + 5, y + 3), "MARKETS", font=SANS_B(7), fill=INK)


def icon_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    s = (h - 18) / 4
    bx, by = x + w / 2 - 2 * s, y + 4
    for r in range(4):
        for c in range(4):
            fill = INK if (r + c) % 2 == 0 else (245, 245, 240)
            d.rectangle([bx + c * s, by + r * s, bx + (c + 1) * s,
                         by + (r + 1) * s], fill=fill)
    d.ellipse([bx + 1.2 * s, by + 0.2 * s, bx + 1.9 * s, by + 0.9 * s],
              fill=(255, 255, 255), outline=INK, width=1)
    d.ellipse([bx + 2.1 * s, by + 2.1 * s, bx + 2.8 * s, by + 2.8 * s],
              fill=INK, outline=(255, 255, 255), width=1)
    d.text((x + 5, y + h - 11), "GENEVA · CHESS", font=SANS_B(7), fill=INK)


def icon_doc(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    px, py = x + w * 0.30, y + 5
    d.rectangle([px, py, px + w * 0.40, y + h - 12], fill=(255, 255, 255),
                outline=INK, width=1)
    for i in range(4):
        ly = py + 7 + i * 8
        d.line([px + 6, ly, px + w * 0.40 - 6, ly], fill=(120, 120, 120),
               width=1)
    d.text((x + 5, y + h - 11), "POLICY", font=SANS_B(7), fill=INK)


def icon_protest(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    for i, px in enumerate((0.18, 0.38, 0.58, 0.78)):
        cx = x + w * px
        d.ellipse([cx - 6, y + h * 0.30, cx + 6, y + h * 0.30 + 12],
                  fill=(200, 170, 130))
        d.rectangle([cx - 8, y + h * 0.30 + 12, cx + 8, y + h - 6],
                    fill=(43, 108, 176) if i % 2 else (179, 53, 43))
    d.rectangle([x + w * 0.10, y + 6, x + w * 0.42, y + 18], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((x + w * 0.12, y + 8), "COST OF LIVING", font=SANS_B(6), fill=INK)
    d.text((x + 5, y + h - 11), "LISBON", font=SANS_B(7), fill=INK)


def icon_ball(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 232, 220))
    cx, cy, r = x + w / 2, y + h / 2 + 2, h * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 200, 60),
              outline=INK, width=1)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=INK, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=INK, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=1)
    d.text((x + 5, y + h - 11), "COURT · BALL", font=SANS_B(7), fill=INK)


def icon_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    d.line([x + w * 0.30, y + 6, x + w * 0.30, y + h - 6], fill=INK, width=2)
    d.polygon([(x + w * 0.30, y + 6), (x + w * 0.78, y + 14),
               (x + w * 0.30, y + 22)], fill=(179, 53, 43))
    d.rectangle([x + w * 0.30, y + h - 8, x + w * 0.70, y + h - 5],
                fill=(120, 110, 95))
    d.text((x + 5, y + h - 11), "POLITICS", font=SANS_B(7), fill=INK)


def icon_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 238))
    cx, cy = x + w / 2, y + h / 2
    d.ellipse([cx - 34, cy - 7, cx + 34, cy + 7], fill=(240, 240, 240),
              outline=INK, width=1)
    d.polygon([(cx + 8, cy - 6), (cx + 26, cy - 22), (cx + 30, cy - 6)],
              fill=(200, 200, 200), outline=INK)
    d.polygon([(cx - 2, cy + 6), (cx + 14, cy + 20), (cx + 20, cy + 6)],
              fill=(200, 200, 200), outline=INK)
    d.polygon([(cx + 30, cy - 4), (cx + 44, cy - 2), (cx + 30, cy + 4)],
              fill=(43, 108, 176))
    for wx in (-24, -12, 0):
        d.ellipse([cx + wx, cy - 3, cx + wx + 5, cy + 2], fill=(43, 108, 176))
    d.text((x + 5, y + h - 11), "O'HARE · CHICAGO", font=SANS_B(7), fill=INK)


# ---------------------------------------------------------------- world map
# Coarse land mask, 72 x 34 cells (5 degrees each), drawn as dots.
MAP_ROWS = [
    "              # #           #                 #       #        #        ",
    "            # # # #       #####       ##       ##        ##      ##      ",
    "  ######## ###############  ######   #   #######################  ##    ",
    "  #########################  #####   # ###################################",
    "   ######  #########    ##  ##      ################################### ",
    "         ################          ## ################################## ",
    "          #############            ## ################################# ",
    "           ############            #################################### ",
    "           ###########             ###################################  ",
    "           ##########             ##  #  ##########################      ",
    "           #########             ##############################         ",
    "            #######              ############ #################         ",
    "            ######                 #################################    ",
    "                 ####              ################################     ",
    "                  ###              #############################  ##    ",
    "                   ###             #########################    ##  # #   ",
    "                    #######        #########################  ######### ",
    "                    ########       ########################  ########## ",
    "                    #########      ########################  ########## ",
    "                    #########       ##########  ##          ########      ",
    "                    #########        ######## ##          ########      ",
    "                     #######         #######              ########   ## ",
    "                     ######           #####                #######   ## ",
    "                     #####                                 ######    ## ",
    "                     ####                                        #    ",
    "                     ###                                         #    ",
    "                     ##                                               ",
    "                                                                        ",
    "                                                                        ",
    "                                                                        ",
    "                                                                        ",
    "                                                                        ",
    "                                                                        ",
    "                                                                        ",
]


def draw_map(d, x, y, w, h, pins):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 242))
    cols, rows = 72, len(MAP_ROWS)
    cw, ch = w / cols, h / rows
    for r, raw in enumerate(MAP_ROWS):
        row = (raw + " " * cols)[:cols]
        for c, cell in enumerate(row):
            if cell == "#":
                cx, cy = x + (c + 0.5) * cw, y + (r + 0.5) * ch
                d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=LAND)
    for n, lon, lat, color in pins:
        px = x + (lon + 180) / 360 * w
        py = y + (85 - lat) / 170 * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=color,
                  outline=(255, 255, 255), width=1)
        f = SANS_B(8)
        s = str(n)
        d.text((px - d.textlength(s, font=f) / 2, py - 5), s, font=f,
               fill=(255, 255, 255))


# ---------------------------------------------------------------- story data
# (number, region, tag, claim_chip, headline, summary, source, illustration)
BIG = [
    (1, "GLOBAL", "MARKETS", "CONFIRMED",
     "Nvidia's Huang returns; shares jump 31%, Wall St rallies",
     "The board reinstates Jensen Huang as CEO 11 days after he stepped "
     "down; Nvidia closes 31% higher and the Nasdaq gains 6.5% in a broad "
     "tech rebound after the worst week since 2020.",
     "Hindu BusinessLine, Reuters", ill_nvidia),
    (2, "ASIA", "DIPLOMACY", "CONFIRMED",
     "Modi and Nepal PM Shah open Saryu-Kamala Express",
     "The two prime ministers virtually flag off the Ayodhya–Janakpur "
     "train and hold bilateral talks on energy, trade and connectivity; "
     "India announces a $1.62bn aid package for flood-hit Nepal.",
     "Jagran Josh, Indian Express", ill_train),
    (3, "EUROPE", "UKRAINE WAR", "CLAIM · KYIV",
     "Russian drone strike hits Kyiv region; several missing",
     "Zelenskyy says a Russian drone strike in the Kyiv region leaves "
     "several people missing; rescuers pull a seven-year-old boy alive "
     "from the rubble of a home in Dymer.",
     "The Guardian, AP", ill_kyiv_hit),
    (4, "ASIA", "DISASTER", "CONFIRMED",
     "Indonesia confirms 24 dead in factory blaze; search goes on",
     "The toll is confirmed after the weekend fire at the PT Fonusa Agung "
     "Mulia candy factory in Cikande, Banten; about 30 people are still "
     "missing and 300 workers were inside when it started.",
     "Reuters, AP", ill_factory_blaze),
]

MED_A = [
    (5, "GLOBAL", "MARKETS", "Nasdaq jumps 6.8% in broad Wall Street rally",
     "The Nasdaq gains 6.8%, the S&P 500 4.7% and the Dow 2.5% as "
     "Nvidia's return lifts chip stocks; the dollar hits a 19-month high.",
     "Reuters", icon_chart),
    (6, "ASIA", "TECH", "Modi opens AI centre at IIT Patna, Rs 400 cr park",
     "The prime minister inaugurates an artificial-intelligence centre "
     "and launches a Rs 400 crore research park project in Bihar.",
     "Times of India", icon_chip),
    (7, "AMERICAS", "TECH", "CrowdStrike to buy Zscaler for $43.9bn",
     "The cybersecurity firm agrees one of the year's biggest tech "
     "takeovers, paying about $43.9 billion for the cloud-security rival.",
     "Reuters", icon_chart),
    (8, "EUROPE", "PROTEST", "Thousands march in Lisbon over living costs",
     "Crowds take to the streets of the Portuguese capital to protest "
     "against rising living costs.",
     "Jagran Josh", icon_protest),
    (9, "SPORT", "CHESS", "Gukesh begins world title defence in Geneva",
     "India's D Gukesh opens his World Chess Championship defence "
     "against Uzbekistan's Javokhir Sindarov.",
     "Times of India", icon_chess),
    (10, "SPORT", "CRICKET", "India–NZ Wellington Test ends in a draw",
     "India declare at a record 720/9 — the highest Test total in New "
     "Zealand — before the first Test is drawn after a visitors' fightback.",
     "Times of India", icon_cricket),
]

MED_B = [
    (11, "ASIA", "WELFARE", "China sets 2030 targets for elderly, childcare",
     "Beijing announces targets to 2030 to strengthen elderly-care "
     "services and childcare support.",
     "Lexington Herald Leader", icon_doc),
    (12, "ASIA", "POLITICS", "Bangladesh vows to arrest Hasina if she returns",
     "Dhaka says former prime minister Sheikh Hasina will be arrested "
     "if she returns from India.",
     "Lexington Herald Leader", icon_flag),
    (13, "EUROPE", "SECURITY", "450 German schools get emailed bomb threats",
     "Around 450 schools across Germany receive bomb threats by email; "
     "police investigate the coordinated messages.",
     "Times of India", icon_flag),
    (14, "AMERICAS", "AVIATION", "O'Hare ground stop briefly halts Chicago flights",
     "Chicago's O'Hare airport issues a brief ground stop over a staffing "
     "shortage at the approach control centre, in Thanksgiving week.",
     "Times of India", icon_plane),
    (15, "SPORT", "TENNIS", "Davis Cup Finals begin in Bologna",
     "Italy begin their title defence at home as the Davis Cup Finals "
     "open in Bologna, running to 29 November.",
     "ATP", icon_ball),
    (16, "SPORT", "BASKETBALL", "Wembanyama's 50 points lift Spurs past Pelicans",
     "Victor Wembanyama scores 50 points with 19 rebounds as San "
     "Antonio beat New Orleans 114–91 to move to 14–3.",
     "NBA", icon_ball),
]

ALSO = [
    (17, "ASIA", "SpiceJet crisis deepens; pilots urge ministry to act"),
    (18, "BUSINESS", "Ferrari unveils 296 Challenge Stradale and Evo in Spain"),
    (19, "ASIA", "South Korea's president names new foreign minister, intel chief"),
    (20, "ASIA", "Armenia proposes new constitution to advance Azerbaijan peace"),
    (21, "MIDDLE EAST", "Oxfam: Gaza war leaves soil, air and water toxic for decades"),
    (22, "ASIA", "Taliban order women's names removed from papers in Balkh"),
    (23, "AMERICAS", "WSJ: Kim Jong Un ignored Trump's repeated outreach"),
    (24, "AMERICAS", "US Senate sets Dec 3 hearing for Nvidia's Huang"),
    (25, "AMERICAS", "Trump hits Newsom in DOJ speech over 548 commuted sentences"),
    (26, "AMERICAS", "Ex-Jackson mayor gets 37 months in bribery case"),
    (27, "AMERICAS", "Kash Patel's $41m fraud probe raids Minnesota child centres"),
    (28, "EUROPE", "King Charles reached out to Meghan after Thomas Markle arrest"),
    (29, "EUROPE", "Dutch activist Bhugwandass dies by euthanasia at 28"),
    (30, "EUROPE", "Russia plans rail ferries to bypass curbs on Kaliningrad link"),
    (31, "ASIA", "Lahore tops world pollution ranking as AQI passes 500"),
    (32, "ASIA", "4.0 quake strikes Pakistan near Afghan border"),
    (33, "ASIA", "Chinese official sentenced to death for leaking 100 reports"),
    (34, "ASIA", "Pakistan to invite India to SCO culture ministers' meet"),
    (35, "ASIA", "Yunus: 'higher level' behind attacks on Grameen Bank branches"),
    (36, "CULTURE", "Mossad saved Swift's Vienna concerts from ISIS plot, ex-chief says"),
    (37, "MARKETS", "Gold rebounds to $3,657 after 14-month low; silver steadies"),
    (38, "MARKETS", "China stocks hit 16-month low; Hang Seng Tech at 26-month low"),
    (39, "AFRICA", "Heavy fighting in Ituri traps DR Congo Ebola responders: WHO"),
    (40, "AFRICA", "Gambia intercepts 491 would-be irregular migrants"),
]

UTC_STRIP = [
    ("Overnight", "Russian drone strike hits Kyiv region"),
    ("Morning", "Modi and Shah flag off Saryu-Kamala Express"),
    ("Midday", "Nvidia shares surge 31% on Huang return"),
    ("Afternoon", "Lisbon marches over cost of living"),
    ("Evening", "Gukesh opens world title defence in Geneva"),
    ("Late", "Davis Cup Finals begin in Bologna"),
]

PINS = [
    (1, -122.0, 37.4, REGION["GLOBAL"]),
    (2, 77.2, 28.6, REGION["ASIA"]),
    (3, 30.5, 50.4, REGION["EUROPE"]),
    (4, 106.1, -6.0, REGION["ASIA"]),
    (5, -74.0, 40.7, REGION["GLOBAL"]),
    (6, 85.1, 25.6, REGION["ASIA"]),
    (7, -77.0, 38.9, REGION["AMERICAS"]),
    (8, -9.1, 38.7, REGION["EUROPE"]),
    (9, 6.1, 46.2, REGION["SPORT"]),
    (10, 174.8, -41.3, REGION["OCEANIA"]),
    (11, 116.4, 39.9, REGION["ASIA"]),
    (12, 90.4, 23.8, REGION["ASIA"]),
    (13, 10.4, 51.2, REGION["EUROPE"]),
    (14, -87.6, 41.9, REGION["AMERICAS"]),
    (15, 11.3, 44.5, REGION["SPORT"]),
    (16, -98.5, 29.4, REGION["SPORT"]),
]


def story_tag(d, x, y, n, region, tag):
    x = num_badge(d, x, y, n, REGION.get(region, INK))
    label = f"{region} · {tag}"
    d.text((x, y + 2), label, font=SANS_B(9), fill=REGION.get(region, INK))
    return x + d.textlength(label, font=SANS_B(9))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- top strip + masthead
    d.text((M, 8), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=SANS_B(11),
           fill=RED)
    right = "40 STORIES · 6 REGIONS · EVERY ONE FROM THIS TUESDAY"
    d.text((W - M - d.textlength(right, font=SANS_B(11)), 8), right,
           font=SANS_B(11), fill=INK)
    d.line([M, 28, W - M, 28], fill=RULE, width=2)
    title = "Tuesday 24 November 2026"
    tf = SERIF_B(54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf,
           fill=INK)
    d.line([M, 98, W - M, 98], fill=RULE, width=2)

    # ---- UTC strip
    y0 = 106
    d.rectangle([M, y0, M + 58, y0 + 44], fill=RED)
    d.text((M + 7, y0 + 6), "THE DAY", font=SANS_B(10), fill=(255, 255, 255))
    d.text((M + 7, y0 + 20), "IN UTC", font=SANS_B(10), fill=(255, 255, 255))
    cell_w = (W - 2 * M - 58) / 6
    for i, (when, what) in enumerate(UTC_STRIP):
        cx = M + 58 + i * cell_w
        if i:
            d.line([cx, y0 + 2, cx, y0 + 42], fill=(200, 200, 200), width=1)
        d.text((cx + 6, y0 + 3), when, font=SANS_B(10), fill=RED)
        text_block(d, cx + 6, y0 + 17, what, COND(9), cell_w - 10,
                   leading=11, max_lines=3)
    d.line([M, y0 + 50, W - M, y0 + 50], fill=RULE, width=1)

    # ---- big four
    y0 = 162
    col_w = (W - 2 * M - 3 * 10) / 4
    for i, (n, region, tag, chip_label, head, summ, src, ill) in enumerate(BIG):
        x = M + i * (col_w + 10)
        ill(d, x, y0, col_w, 92)
        ty = y0 + 96
        tx = story_tag(d, x, ty, n, region, tag)
        chip(d, tx + 6, ty + 1, chip_label, GRAY)
        hy = text_block(d, x, ty + 18, head, SERIF_B(15), col_w, leading=17,
                        max_lines=3)
        sy = text_block(d, x, hy + 2, summ, COND(9.5), col_w, fill=(50, 50, 50),
                        leading=11, max_lines=4)
        d.text((x, sy + 1), src, font=COND(8), fill=GRAY)
    d.line([M, 376, W - M, 376], fill=RULE, width=1)

    # ---- medium rows
    def med_row(y0, stories):
        col_w = (W - 2 * M - 5 * 8) / 6
        for i, (n, region, tag, head, summ, src, icon) in enumerate(stories):
            x = M + i * (col_w + 8)
            icon(d, x, y0, col_w, 54)
            ty = y0 + 58
            story_tag(d, x, ty, n, region, tag)
            hy = text_block(d, x, ty + 16, head, SERIF_B(11), col_w,
                            leading=12, max_lines=3)
            sy = text_block(d, x, hy + 1, summ, COND(8.5), col_w,
                            fill=(50, 50, 50), leading=10, max_lines=4)
            d.text((x, sy + 1), src, font=COND(7.5), fill=GRAY)

    med_row(384, MED_A)
    d.line([M, 536, W - M, 536], fill=RULE, width=1)
    med_row(544, MED_B)
    d.line([M, 696, W - M, 696], fill=RULE, width=1)

    # ---- bottom: map + also-on list
    y0 = 704
    d.text((M, y0), "WHERE IT HAPPENED", font=SANS_B(10), fill=INK)
    draw_map(d, M, y0 + 16, 320, 150, PINS)
    legend = [("EUROPE", "Europe"), ("MIDDLE EAST", "Middle East"),
              ("ASIA", "Asia"), ("AMERICAS", "Americas"),
              ("AFRICA", "Africa"), ("OCEANIA", "Oceania")]
    lx = M
    for key, name in legend:
        d.ellipse([lx, y0 + 172, lx + 7, y0 + 179], fill=REGION[key])
        d.text((lx + 10, y0 + 171), name, font=COND(8), fill=INK)
        lx += 12 + d.textlength(name, font=COND(8)) + 8

    ax = M + 336
    d.text((ax, y0), "ALSO ON TUESDAY 24 NOVEMBER", font=SANS_B(10), fill=INK)
    acol_w = (W - M - ax - 2 * 10) / 3
    per_col = 8
    for ci in range(3):
        cx = ax + ci * (acol_w + 10)
        cy = y0 + 18
        for (n, region, line) in ALSO[ci * per_col:(ci + 1) * per_col]:
            num_badge(d, cx, cy, n, REGION.get(region, INK))
            cy = text_block(d, cx + 19, cy + 1, line, COND(8.5),
                            acol_w - 19, leading=10, max_lines=3) + 4

    # ---- date check
    y0 = 928
    d.rectangle([M, y0, W - M, y0 + 58], outline=RED, width=1)
    d.rectangle([M, y0, M + 92, y0 + 58], fill=RED)
    d.text((M + 8, y0 + 8), "DATE", font=SANS_B(13), fill=(255, 255, 255))
    d.text((M + 8, y0 + 26), "CHECK", font=SANS_B(13), fill=(255, 255, 255))
    dc = ("Left out on purpose because they broke before Tuesday: "
          "COP31 collapsing with no deal in Antalya (22 Nov), the Russian "
          "corvette sunk at Benghazi (22 Nov), the Kyiv apartment-block "
          "strike (22 Nov), Alcaraz's ATP Finals title (22 Nov), "
          "Verstappen's Las Vegas GP win (22 Nov), Liverpool 4–0 Man Utd "
          "(22 Nov), BepiColombo reaching Mercury orbit (21 Nov). Not yet: "
          "Germany's Ifo business index, due 10:30 CET today.")
    text_block(d, M + 102, y0 + 6, dc, COND(10), W - 2 * M - 112, leading=13,
               max_lines=4)

    # ---- footer
    foot = ("Every story here happened or was first reported on Tuesday 24 "
            "November 2026. CLAIM = one side's account, not independently "
            "confirmed. Sources: The Hindu BusinessLine, Reuters, Times of "
            "India, Jagran Josh, AP, The Guardian, PANA. Original drawings.")
    text_block(d, M, 992, foot, COND(9), W - 2 * M, fill=GRAY, leading=11,
               max_lines=3)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
