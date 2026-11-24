"""Render one day of world news as a single newspaper picture.

Tuesday 24 November 2026. Pure Pillow + stdlib, no network at runtime,
fully deterministic: same input, same bytes, every run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (248, 243, 230)
INK = (26, 26, 26)
RED = (163, 22, 33)
GREEN = (31, 122, 62)
ORANGE = (198, 96, 20)
GRAY = (112, 107, 96)
LIGHT = (233, 226, 210)
NAVY = (16, 26, 46)
SKY = (176, 206, 222)
MAPGREEN = (104, 138, 102)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    try:
        return ImageFont.truetype(os.path.join(FD, name), size)
    except OSError:
        return ImageFont.truetype(os.path.join(FD, "DejaVuSans.ttf"), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_O = "DejaVuSans-Oblique.ttf"


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, lines, font, fill, leading):
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, color):
    f = F(SANS_B, 9)
    w = d.textlength(text, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3,
                        outline=color, width=1)
    d.text((x + 5, y + 2), text, font=f, fill=color)
    return x + w


def badge(d, x, y, num, r=8):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = F(SANS_B, 10)
    t = str(num)
    tw = d.textlength(t, font=f)
    d.text((x + r - tw / 2, y + r - 6), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- stories
BIG = [
    dict(num=1, cat="GLOBAL · MARKETS", chip="CONFIRMED", chipc=GREEN,
         head="Nvidia's Huang returns; shares jump 31%, Wall St rallies",
         body=("The board reinstates Jensen Huang as CEO 11 days after he "
               "stepped down. Nvidia closes 31% higher and the Nasdaq gains "
               "6.8% in a broad tech rebound after the worst week since 2020."),
         src="AP, Reuters", art="chart"),
    dict(num=2, cat="ASIA · DIPLOMACY", chip="CONFIRMED", chipc=GREEN,
         head="Modi and Nepal PM Shah open Saryu-Kamala Express",
         body=("The two prime ministers virtually flag off the Ayodhya–Janakpur "
               "train and hold bilateral talks on energy, trade and "
               "connectivity; India announces a $1.62bn package for Nepal."),
         src="Jagran Josh, Indian Express", art="train"),
    dict(num=3, cat="EUROPE · UKRAINE WAR", chip="CLAIM · KYIV", chipc=ORANGE,
         head="Russian drone strike hits Kyiv region; several missing",
         body=("Zelenskyy says a Russian drone strike in the Kyiv region "
               "leaves several people missing; rescuers pull a seven-year-old "
               "boy alive from the rubble of a home in Dymer."),
         src="The Guardian, AP", art="building"),
    dict(num=4, cat="ASIA · DISASTER", chip="CONFIRMED", chipc=GREEN,
         head="Indonesia confirms 24 dead in factory blaze; search goes on",
         body=("The toll is confirmed after the weekend fire at the PT Fonusa "
               "Agung Mulia candy factory in Cikande, Banten; about 30 people "
               "are still missing and 300 workers were inside when it started."),
         src="Reuters, AP", art="factory"),
]

MED = [
    dict(num=5, cat="GLOBAL · MARKETS",
         head="Nasdaq jumps 6.8% in broad Wall Street rally",
         body=("The Nasdaq gains 6.8%, the S&P 500 4.7% and the Dow 2.9% as "
               "Nvidia's return lifts beaten-down AI stocks."),
         src="Reuters", art="bars"),
    dict(num=6, cat="ASIA · TECH",
         head="Modi opens AI centre at IIT Patna, Rs 400 cr park",
         body=("The prime minister inaugurates an artificial intelligence "
               "centre and launches a Rs 400 crore research park in Bihar."),
         src="Times of India", art="chip"),
    dict(num=7, cat="AMERICAS · TECH",
         head="CrowdStrike to buy Zscaler for $43.9bn",
         body=("The cybersecurity firm agrees one of the largest tech "
               "takeovers, paying about $43.9bn for the cloud-security rival."),
         src="Reuters", art="deal"),
    dict(num=8, cat="EUROPE · PROTEST",
         head="Thousands march in Lisbon over living costs",
         body=("Crowds take to the streets of the Portuguese capital to "
               "protest against the cost of living and demand higher pay."),
         src="Jagran Josh", art="crowd"),
    dict(num=9, cat="SPORT · CHESS",
         head="Gukesh begins world title defence in Geneva",
         body=("India's D. Gukesh opens his World Chess Championship defence "
               "against Uzbekistan's Javokhir Sindarov."),
         src="Times of India", art="chess"),
    dict(num=10, cat="SPORT · CRICKET",
         head="India–NZ Wellington Test ends in a draw",
         body=("India declare at a record 720/9 — the highest Test total in "
               "New Zealand — before the first Test is drawn."),
         src="Times of India", art="ball"),
    dict(num=11, cat="ASIA · WELFARE",
         head="China sets 2030 targets for elderly, childcare",
         body=("Beijing announces targets to 2030 to strengthen elderly-care "
               "services and childcare support."),
         src="Lexington Herald Leader", art="doc"),
    dict(num=12, cat="ASIA · POLITICS",
         head="Bangladesh vows to arrest Hasina if she returns",
         body=("Dhaka says former prime minister Sheikh Hasina will be "
               "arrested if she returns from India."),
         src="Lexington Herald Leader", art="flag"),
    dict(num=13, cat="EUROPE · SECURITY",
         head="450 German schools get emailed bomb threats",
         body=("Schools in several states across Germany receive bomb threats "
               "by email; police investigate the coordinated messages."),
         src="Times of India", art="shield"),
    dict(num=14, cat="AMERICAS · AVIATION",
         head="O'Hare ground stop briefly halts Chicago flights",
         body=("Chicago's O'Hare airport issues a brief ground stop over a "
               "staffing shortage at the approach control centre."),
         src="Times of India", art="plane"),
    dict(num=15, cat="SPORT · TENNIS",
         head="Davis Cup Finals begin in Bologna",
         body=("Italy begin their title defence at home as the Davis Cup "
               "Finals open in Bologna, running to 29 November."),
         src="ATP", art="tennis"),
    dict(num=16, cat="SPORT · BASKETBALL",
         head="Wembanyama's 50 points lift Spurs past Pelicans",
         body=("Victor Wembanyama scores 50 points with 19 rebounds as San "
               "Antonio beat New Orleans 114–91 to move to 14–3."),
         src="NBA", art="hoop"),
]

ONELINERS = [
    "SpiceJet crisis deepens; pilots urge ministry to act",
    "Ferrari unveils 296 Challenge Stradale and Evo in Spain",
    "South Korea's president names new foreign minister, intel chief",
    "Armenia proposes new constitution to advance Azerbaijan peace",
    "Oxfam: Gaza war leaves soil, air and water toxic",
    "Taliban order women's names removed from papers in Balkh",
    "WSJ: Kim Jong Un ignored Trump's repeated outreach",
    "US Senate sets Dec 3 hearing for Nvidia's Huang",
    "Trump hits Newsom in DOJ speech over 548 commuted sentences",
    "Ex-Jackson mayor gets 37 months in bribery case",
    "Kash Patel's $41m fraud probe raids Minnesota child centres",
    "King Charles reached out to Meghan after Thomas Markle arrest",
    "Dutch activist Bhugwandass dies by euthanasia at 41",
    "Russia plans rail ferries to bypass curbs on Kaliningrad link",
    "Lahore tops world pollution ranking as AQI passes 500",
    "4.0 quake strikes Pakistan near Afghan border",
    "Chinese official sentenced to death for leaking 100 reports",
    "Pakistan to invite India to SCO culture ministers' meet",
    "Yunus: 'higher level' behind attacks on Grameen Bank",
    "Mossad saved Swift's Vienna concerts from ISIS plot, ex-chief says",
    "Gold rebounds to $3,657 after 14-month low; silver steadies",
    "China stocks hit 16-month low; Hang Seng Tech at 26-month low",
    "Heavy fighting in Ituri traps DR Congo Ebola responders: WHO",
    "Gambia intercepts 491 would-be irregular migrants",
]

TIMELINE = [
    ("Overnight", "Russian drone strike hits Kyiv region"),
    ("Morning", "Modi and Shah flag off Saryu-Kamala Express"),
    ("Midday", "Nvidia +31% as Huang returns"),
    ("Afternoon", "Lisbon marches over cost of living"),
    ("Evening", "Gukesh opens world title defence in Geneva"),
    ("Late", "Davis Cup Finals begin in Bologna"),
]

DATECHECK = ("Left out on purpose because they broke before Tuesday: COP31 "
             "collapsing with no deal in Antalya (22 Nov), the Russian corvette "
             "sunk at Benghazi (22 Nov), Alcaraz's ATP Finals title (22 Nov), "
             "Verstappen's Las Vegas GP win (22 Nov), Liverpool 4–0 Man Utd "
             "(22 Nov), BepiColombo reaching Mercury orbit (21 Nov). Not yet: "
             "Germany's Ifo business index, due 10:30 CET today.")

# coarse dotted world map: (row, col_start, col_end), 30 rows x 72 cols
LAND = [
    (2, 22, 25), (3, 4, 10), (3, 44, 68),
    (4, 4, 12), (4, 36, 39), (4, 44, 68),
    (5, 8, 20), (5, 33, 39), (5, 44, 67),
    (6, 8, 20), (6, 33, 40), (6, 44, 66),
    (7, 8, 20), (7, 34, 40), (7, 44, 62),
    (8, 8, 19), (8, 33, 40), (8, 41, 45), (8, 47, 60),
    (9, 8, 18), (9, 41, 45), (9, 47, 58),
    (10, 8, 15), (10, 41, 44), (10, 47, 56),
    (11, 8, 13), (11, 34, 42), (11, 47, 55),
    (12, 10, 14), (12, 35, 42), (12, 53, 57),
    (13, 13, 16), (13, 36, 42), (13, 54, 58),
    (14, 15, 19), (14, 36, 42), (14, 55, 60),
    (15, 15, 19), (15, 36, 42),
    (16, 16, 19), (16, 36, 41),
    (17, 16, 19), (17, 36, 41),
    (18, 16, 19), (18, 36, 40),
    (19, 17, 19), (19, 37, 40),
    (20, 17, 18), (20, 37, 39), (20, 58, 66),
    (21, 17, 18), (21, 58, 65),
    (22, 17, 18), (22, 59, 64),
    (23, 18, 18), (23, 60, 63),
    (24, 18, 18),
]

PINS = [  # (story num, lon, lat)
    (1, -122.0, 37.4), (2, 82.2, 26.8), (3, 30.5, 50.8),
    (4, 106.2, -6.3), (5, -74.0, 40.7), (6, 85.1, 25.6),
    (7, -97.7, 30.3), (8, -9.1, 38.7), (9, 6.1, 46.2),
    (10, 174.8, -41.3), (11, 116.4, 39.9), (12, 90.4, 23.8),
    (13, 13.4, 52.5), (14, -87.6, 41.9), (15, 11.3, 44.5),
    (16, -98.5, 29.4),
]


# ---------------------------------------------------------------- artwork
def art_big(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    if kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(12, 20, 38))
        pts = [(x + 12, y + h - 18), (x + 55, y + h - 42), (x + 95, y + h - 30),
               (x + 135, y + h - 58), (x + 175, y + h - 44), (x + w - 14, y + 16)]
        d.line(pts, fill=(46, 204, 113), width=4)
        d.polygon(pts + [(x + w - 14, y + h), (x + 12, y + h)],
                  fill=(46, 204, 113, 40))
        d.text((x + 12, y + 10), "NVDA", font=F(SANS_B, 11), fill=(150, 200, 255))
        d.text((x + 12, y + 26), "SANTA CLARA · CHIP MAKER",
               font=F(SANS_B, 8), fill=(160, 170, 190))
        d.text((x + w - 108, y + h - 34), "+31%", font=F(SANS_B, 26),
               fill=(255, 255, 255))
    elif kind == "train":
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=(250, 214, 120))
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 150, 120))
        for i, col in enumerate([(178, 34, 34), (40, 70, 140), (220, 170, 40)]):
            cx = x + 14 + i * 74
            d.rectangle([cx, y + 44, cx + 66, y + 78], fill=col)
            for wx in range(3):
                d.rectangle([cx + 8 + wx * 20, y + 52, cx + 22 + wx * 20, y + 64],
                            fill=(230, 240, 250))
            d.ellipse([cx + 10, y + 78, cx + 20, y + 88], fill=(30, 30, 30))
            d.ellipse([cx + 46, y + 78, cx + 56, y + 88], fill=(30, 30, 30))
        d.text((x + 12, y + h - 16), "AYODHYA – JANAKPUR",
               font=F(SANS_B, 8), fill=(60, 60, 60))
    elif kind == "building":
        d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
        d.ellipse([x + 150, y + 6, x + 178, y + 26], fill=(120, 120, 120))
        d.ellipse([x + 186, y + 14, x + 206, y + 30], fill=(100, 100, 100))
        d.rectangle([x + 30, y + 30, x + 150, y + h - 8], fill=(70, 66, 60))
        for r in range(4):
            for c in range(5):
                lit = (r + c) % 3 != 0
                d.rectangle([x + 40 + c * 22, y + 40 + r * 16,
                             x + 54 + c * 22, y + 52 + r * 16],
                            fill=(250, 200, 90) if lit else (40, 40, 44))
        d.polygon([(x + 150, y + 30), (x + w - 8, y + 44), (x + w - 8, y + 84),
                   (x + 150, y + 74)], fill=(250, 214, 120))
        d.text((x + 12, y + 8), "DYMER · KYIV REGION",
               font=F(SANS_B, 8), fill=(200, 200, 200))
    elif kind == "factory":
        d.rectangle([x, y, x + w, y + h], fill=(26, 22, 26))
        d.ellipse([x + 60, y + h - 52, x + 190, y + h + 10], fill=(220, 110, 30))
        d.rectangle([x + 20, y + 62, x + 150, y + h - 6], fill=(52, 44, 44))
        d.rectangle([x + 160, y + 34, x + 176, y + h - 6], fill=(52, 44, 44))
        d.rectangle([x + 186, y + 46, x + 200, y + h - 6], fill=(52, 44, 44))
        for wx in range(4):
            d.rectangle([x + 30 + wx * 28, y + 70, x + 46 + wx * 28, y + 86],
                        fill=(250, 180, 80))
        d.ellipse([x + 158, y + 12, x + 180, y + 32], fill=(140, 140, 140))
        d.text((x + 12, y + 8), "CIKANDE · BANTEN",
               font=F(SANS_B, 8), fill=(200, 200, 200))


def art_small(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    cx, cy = x + w / 2, y + h / 2
    if kind == "bars":
        base = y + h - 8
        for i, bh in enumerate([10, 18, 14, 24, 30]):
            d.rectangle([x + 14 + i * 26, base - bh, x + 32 + i * 26, base],
                        fill=(31, 122, 62))
    elif kind == "chip":
        d.rectangle([x + w / 2 - 34, y + 6, x + w / 2 + 34, y + h - 6],
                    fill=(30, 50, 110))
        d.text((cx - 12, cy - 9), "AI", font=F(SANS_B, 16), fill=(255, 255, 255))
    elif kind == "deal":
        d.rectangle([x + 20, y + 8, x + 70, y + h - 8], fill=(40, 70, 140))
        d.rectangle([x + 90, y + 8, x + 140, y + h - 8], fill=(31, 122, 62))
        d.text((cx - 8, cy - 9), "+", font=F(SANS_B, 18), fill=INK)
    elif kind == "crowd":
        for i, col in enumerate([(40, 70, 140), (178, 34, 34), (40, 70, 140),
                                 (220, 170, 40), (40, 70, 140)]):
            px = x + 22 + i * 28
            d.ellipse([px - 7, y + 8, px + 7, y + 22], fill=col)
            d.rectangle([px - 9, y + 24, px + 9, y + h - 6], fill=col)
    elif kind == "chess":
        s = 9
        for r in range(4):
            for c in range(4):
                col = (30, 30, 30) if (r + c) % 2 == 0 else (240, 240, 240)
                d.rectangle([x + w / 2 - 18 + c * s, y + 2 + r * s,
                             x + w / 2 - 18 + (c + 1) * s, y + 2 + (r + 1) * s],
                            fill=col)
    elif kind == "ball":
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(200, 40, 40))
        d.arc([cx - 14, cy - 14, cx + 14, cy + 14], 200, 340, fill=(255, 255, 255),
              width=2)
    elif kind == "doc":
        d.rectangle([x + w / 2 - 22, y + 4, x + w / 2 + 22, y + h - 4],
                    fill=(255, 255, 255), outline=GRAY)
        for i in range(4):
            d.line([x + w / 2 - 16, y + 10 + i * 7, x + w / 2 + 16, y + 10 + i * 7],
                   fill=GRAY, width=2)
    elif kind == "flag":
        d.rectangle([x + w / 2 - 2, y + 4, x + w / 2 + 2, y + h - 4], fill=INK)
        d.polygon([(x + w / 2 + 2, y + 5), (x + w / 2 + 40, y + 12),
                   (x + w / 2 + 2, y + 20)], fill=RED)
    elif kind == "shield":
        d.polygon([(cx, y + 4), (cx + 20, y + 10), (cx + 20, y + 22),
                   (cx, y + h - 4), (cx - 20, y + 22), (cx - 20, y + 10)],
                  fill=(40, 70, 140))
        d.text((cx - 5, cy - 8), "!", font=F(SANS_B, 16), fill=(255, 255, 255))
    elif kind == "plane":
        d.polygon([(x + 30, cy), (x + w - 30, cy - 10), (x + w - 14, cy),
                   (x + w - 30, cy + 10)], fill=(90, 110, 140))
        d.polygon([(x + 70, cy - 4), (x + 96, cy - 16), (x + 100, cy - 4)],
                  fill=(90, 110, 140))
    elif kind == "tennis":
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(200, 220, 60))
        d.arc([cx - 14, cy - 14, cx + 14, cy + 14], 60, 300, fill=(255, 255, 255),
              width=2)
    elif kind == "hoop":
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(230, 120, 40))
        d.line([cx - 14, cy, cx + 14, cy], fill=(120, 60, 20), width=2)
        d.line([cx, cy - 14, cx, cy + 14], fill=(120, 60, 20), width=2)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14
    CW = W - 2 * M

    # top bar
    d.text((M, 8), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=F(SANS_B, 10), fill=INK)
    rt = "40 STORIES · 6 REGIONS · EVERY ONE FROM THIS TUESDAY"
    d.text((W - M - d.textlength(rt, font=F(SANS_B, 10)), 8), rt,
           font=F(SANS_B, 10), fill=INK)
    d.line([(M, 26), (W - M, 26)], fill=RED, width=2)

    # masthead
    title = "Tuesday 24 November 2026"
    tf = F(SERIF_B, 54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 32), title, font=tf, fill=INK)
    d.line([(M, 96), (W - M, 96)], fill=INK, width=1)
    d.line([(M, 99), (W - M, 99)], fill=INK, width=1)

    # timeline strip
    ty, th = 104, 38
    d.rectangle([M, ty, M + 116, ty + th], fill=RED)
    d.text((M + 8, ty + 5), "THE DAY", font=F(SANS_B, 12), fill=(255, 255, 255))
    d.text((M + 8, ty + 20), "IN UTC", font=F(SANS_B, 12), fill=(255, 255, 255))
    cellw = (CW - 116 - 6) / 6
    for i, (lab, txt) in enumerate(TIMELINE):
        cx = M + 116 + 6 + i * cellw
        d.text((cx, ty + 2), lab.upper(), font=F(SANS_B, 9), fill=RED)
        lines = wrap(d, txt, F(SANS, 10), cellw - 4)
        block(d, cx, ty + 15, lines[:2], F(SANS, 10), INK, 12)

    # big cards
    by, bh = 148, 248
    gap = 6
    bw = (CW - 3 * gap) / 4
    for i, s in enumerate(BIG):
        x = M + i * (bw + gap)
        art_big(d, x, by, bw, 104, s["art"])
        my = by + 110
        badge(d, x, my, s["num"])
        d.text((x + 20, my + 2), s["cat"], font=F(SANS_B, 9), fill=INK)
        chip(d, x + 20 + d.textlength(s["cat"], font=F(SANS_B, 9)) + 6, my,
             s["chip"], s["chipc"])
        lines = wrap(d, s["head"], F(SERIF_B, 15), bw - 2)
        block(d, x, my + 20, lines[:3], F(SERIF_B, 15), INK, 18)
        blines = wrap(d, s["body"], F(SANS, 10), bw - 2)
        block(d, x, my + 76, blines[:4], F(SANS, 10), INK, 12)
        d.text((x, by + bh - 10), s["src"], font=F(SANS_O, 9), fill=GRAY)

    # medium cards, two rows of six
    mw = (CW - 5 * gap) / 6
    for row in range(2):
        ry = 402 + row * 118
        for col in range(6):
            s = MED[row * 6 + col]
            x = M + col * (mw + gap)
            art_small(d, x, ry, mw, 36, s["art"])
            my = ry + 40
            badge(d, x, my, s["num"], r=7)
            d.text((x + 17, my + 1), s["cat"], font=F(SANS_B, 8), fill=INK)
            lines = wrap(d, s["head"], F(SERIF_B, 11), mw - 2)
            block(d, x, my + 15, lines[:2], F(SERIF_B, 11), INK, 13)
            blines = wrap(d, s["body"], F(SANS, 8), mw - 2)
            block(d, x, my + 42, blines[:2], F(SANS, 8), INK, 10)
            d.text((x, ry + 106), s["src"], font=F(SANS_O, 8), fill=GRAY)

    # map + one-liners
    ly = 640
    d.text((M, ly), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
    d.text((M + 348, ly), "ALSO ON TUESDAY 24 NOVEMBER",
           font=F(SANS_B, 12), fill=INK)
    mx, my0, mw2, mh2 = M, ly + 20, 330, 262
    d.rectangle([mx, my0, mx + mw2, my0 + mh2], outline=GRAY, width=1)
    gx, gy = mx + 6, my0 + 8
    cellw, cellh = (mw2 - 12) / 72, (mh2 - 40) / 30
    for (r, c0, c1) in LAND:
        for c in range(c0, c1 + 1):
            px = gx + (c + 0.5) * cellw
            py = gy + (r + 0.5) * cellh
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=MAPGREEN)
    for num, lon, lat in PINS:
        px = gx + (lon + 180) / 360 * (mw2 - 12)
        py = gy + (85 - lat) / 145 * (mh2 - 40)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = F(SANS_B, 8)
        t = str(num)
        d.text((px - d.textlength(t, font=f) / 2, py - 5), t, font=f,
               fill=(255, 255, 255))
    leg_y = my0 + mh2 - 26
    for i, (col, name) in enumerate([(RED, "Europe"), ((198, 96, 20), "Middle East"),
                                     (MAPGREEN, "Asia"), ((40, 70, 140), "Americas"),
                                     ((120, 60, 160), "Africa"), ((90, 110, 140), "Oceania")]):
        lx = mx + 8 + i * 55
        d.ellipse([lx, leg_y, lx + 7, leg_y + 7], fill=col)
        d.text((lx + 10, leg_y - 1), name, font=F(SANS, 8), fill=INK)

    # one-liners, two columns
    colw = (CW - 348 - 10) / 2
    for ci in range(2):
        cx = M + 348 + ci * (colw + 10)
        for ri in range(12):
            n = 17 + ci * 12 + ri
            txt = ONELINERS[n - 17]
            iy = ly + 20 + ri * 22
            fnum = F(SANS_B, 10)
            d.text((cx, iy), str(n), font=fnum, fill=RED)
            lines = wrap(d, txt, F(SANS, 9), colw - 26)
            block(d, cx + 26, iy + 1, lines[:2], F(SANS, 9), INK, 11)

    # date check
    dy = 922
    d.rectangle([M, dy, M + 88, dy + 62], fill=RED)
    d.text((M + 10, dy + 10), "DATE", font=F(SANS_B, 13), fill=(255, 255, 255))
    d.text((M + 10, dy + 28), "CHECK", font=F(SANS_B, 13), fill=(255, 255, 255))
    d.rectangle([M + 88, dy, W - M, dy + 62], outline=RED, width=1)
    lines = wrap(d, DATECHECK, F(SANS, 10), CW - 88 - 16)
    block(d, M + 96, dy + 6, lines[:4], F(SANS, 10), INK, 13)

    # footer
    d.text((M, 992),
           "Every story here happened or was first reported on Tuesday 24 November 2026. "
           "CLAIM = one side's account, not independently confirmed.",
           font=F(SANS, 8), fill=GRAY)
    d.text((M, 1004),
           "Sources: AP, Reuters, The Guardian, Times of India, Jagran Josh, ATP, NBA. "
           "Original drawings.",
           font=F(SANS, 8), fill=GRAY)
    d.rectangle([0, 0, W - 1, H - 1], outline=RED, width=3)
    return img


if __name__ == "__main__":
    build().save("/tmp/preview.png")
