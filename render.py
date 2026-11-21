#!/usr/bin/env python3
"""Render the news-image-20261120 round 2 entry: a dense one-page newspaper
front page summing up Friday 20 November 2026. All drawings are original
vector-style art made with Pillow; every word is set in DejaVu/Liberation
fonts, so no text is ever garbled. Output: entry.png, 1024x1024, < 1 MiB."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (154, 20, 26)
DARKRED = (122, 12, 18)
BLUE = (29, 53, 87)
TEAL = (15, 118, 110)
GOLD = (180, 83, 9)
GREEN = (34, 100, 60)
PURPLE = (107, 70, 150)
GREY = (107, 107, 107)
RULE = (60, 60, 60)
NAVY = (16, 38, 66)
SEA = (22, 50, 79)
LAND = (217, 201, 163)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def font(path, size):
    return ImageFont.truetype(path, size)


SERIF = FD + "DejaVuSerif.ttf"
SERIFB = FD + "DejaVuSerif-Bold.ttf"
SERIFI = FL + "LiberationSerif-Italic.ttf"
SANS = FD + "DejaVuSans.ttf"
SANSB = FD + "DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)


def centre(x, y, s, fnt, fill=INK):
    d.text((x, y), s, font=fnt, fill=fill, anchor="ma")


def hline(y, x0=12, x1=1012, wdt=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def banner(x, y, w_, h_, s, fnt, bg=RED, fg=(255, 255, 255)):
    d.rectangle([x, y, x + w_, y + h_], fill=bg)
    d.text((x + w_ / 2, y + h_ / 2), s, font=fnt, fill=fg, anchor="mm")


def burst(cx, cy, r, fill=(255, 170, 0), core=(255, 230, 120)):
    """Explosion starburst: radiating triangles + bright core."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)
    d.ellipse([cx - r * 0.38, cy - r * 0.38, cx + r * 0.38, cy + r * 0.38],
              fill=core)


def big_panel(x, y, w_, num, kicker, headline, caption):
    """A lead panel: image box drawn by caller sits above; this adds the
    kicker, headline and caption below the image box."""
    text(x, y, f"{num}  ·  {kicker}", font(SANSB, 11), fill=RED)
    lines = wrap(headline, font(SERIFB, 20), w_)
    yy = y + 16
    for ln in lines[:2]:
        text(x, yy, ln, font(SERIFB, 20))
        yy += 23
    clines = wrap(caption, font(SANS, 12), w_)
    for ln in clines[:3]:
        text(x, yy, ln, font(SANS, 12))
        yy += 15
    return yy


def small_panel(x, y, w_, num, kicker, headline, caption):
    text(x, y, f"{num}  ·  {kicker}", font(SANSB, 10), fill=RED)
    lines = wrap(headline, font(SERIFB, 15), w_)
    yy = y + 14
    for ln in lines[:2]:
        text(x, yy, ln, font(SERIFB, 15))
        yy += 18
    clines = wrap(caption, font(SANS, 10), w_)
    for ln in clines[:2]:
        text(x, yy, ln, font(SANS, 10))
        yy += 13
    return yy


# ---------------------------------------------------------------- top bar
text(12, 6, "THE WORLD IN ONE DAY", font(SANSB, 13), fill=RED)
text(1012, 6, "35 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED FRIDAY 20 NOVEMBER 2026",
     font(SANSB, 11), anchor="ra")
hline(26)

# ---------------------------------------------------------------- masthead
centre(512, 30, "Friday 20 November 2026", font(SERIFB, 62))
centre(512, 100,
       "Russian missiles hit Kyiv\u2019s bridges  \u00b7  Cyclone Akvan strikes India  "
       "\u00b7  AI sell-off sinks Asia  \u00b7  UK and EU seal a deal",
       font(SERIFI, 16))
hline(122, wdt=3)
hline(126, wdt=1)

# ---------------------------------------------------------------- numbers
NUMBERS = [
    ("100+", "missiles fired at Ukraine overnight"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("\u22126.2%", "Taiwan\u2019s index at Friday\u2019s close"),
    ("100,000", "youth visas a year in the UK\u2013EU deal"),
    ("2.3%", "Japan consumer inflation, October"),
    ("118", "Phillips runs against India"),
]
cell_w = (1024 - 24) / 6
for i, (big, small) in enumerate(NUMBERS):
    cx = 12 + i * cell_w
    if i:
        d.line([(cx, 132), (cx, 168)], fill=(180, 170, 150), width=1)
    centre(cx + cell_w / 2, 128, big, font(SERIFB, 24), fill=RED)
    for j, ln in enumerate(wrap(small, font(SANS, 10), cell_w - 12)):
        centre(cx + cell_w / 2, 154 + j * 12, ln, font(SANS, 10))

# ---------------------------------------------------------------- region bar
REGIONS = [("EUROPE 9", RED), ("ASIA 9", TEAL), ("AMERICAS 6", BLUE),
           ("MIDDLE EAST 3", GOLD), ("AFRICA 3", GREEN), ("OCEANIA 2", PURPLE),
           ("GLOBAL 3", GREY)]
rx = 12
for label, col in REGIONS:
    w_ = d.textlength(label, font=font(SANSB, 11)) + 22
    d.rectangle([rx, 178, rx + w_, 196], fill=col)
    centre(rx + w_ / 2, 181, label, font(SANSB, 11), fill=(255, 255, 255))
    rx += w_ + 4

# ---------------------------------------------------------------- big row
BIG_Y, BIG_H, BIG_W, GAP = 202, 122, 328, 8
big_x = [12, 12 + BIG_W + GAP, 12 + 2 * (BIG_W + GAP)]

# --- 1. KYIV: night skyline, river bridges, missile arcs, explosions
x0 = big_x[0]
d.rectangle([x0, BIG_Y, x0 + BIG_W, BIG_Y + BIG_H], fill=(11, 30, 58))
for sx, sy in [(20, 14), (70, 26), (130, 10), (200, 22), (260, 12), (300, 30),
               (45, 40), (160, 34), (235, 8), (290, 44)]:
    d.ellipse([x0 + sx, BIG_Y + sy, x0 + sx + 2, BIG_Y + sy + 2], fill=(255, 255, 200))
# skyline
for bx, bw, bh in [(0, 34, 52), (36, 26, 68), (64, 40, 46), (106, 30, 74),
                   (138, 34, 56), (174, 28, 66), (204, 36, 48), (242, 30, 70),
                   (274, 28, 54), (304, 24, 62)]:
    d.rectangle([x0 + bx, BIG_Y + BIG_H - 34 - bh, x0 + bx + bw,
                 BIG_Y + BIG_H - 30], fill=(18, 41, 77))
    for wy in range(BIG_Y + BIG_H - 30 - bh + 8, BIG_Y + BIG_H - 32, 12):
        for wx in range(bx + 5, bx + bw - 4, 10):
            if (wx + wy) % 3 == 0:
                d.rectangle([x0 + wx, wy, x0 + wx + 3, wy + 4], fill=(255, 205, 90))
# river
d.rectangle([x0, BIG_Y + BIG_H - 30, x0 + BIG_W, BIG_Y + BIG_H], fill=(29, 78, 137))
# bridge deck + arches
by = BIG_Y + BIG_H - 30
d.line([(x0, by), (x0 + BIG_W, by)], fill=(200, 200, 200), width=3)
for ax in (40, 150, 260):
    d.arc([x0 + ax - 45, by - 26, x0 + ax + 45, by + 8], 180, 360,
          fill=(200, 200, 200), width=3)
    d.line([(x0 + ax, by - 26), (x0 + ax, by)], fill=(200, 200, 200), width=2)
# dashed missile arcs
for (ax0, ay0, ax1, ay1) in [(300, 6, 190, 66), (250, 2, 90, 78), (320, 30, 250, 60)]:
    for t in [i / 24 for i in range(25)]:
        if i % 2 == 0:
            px = x0 + ax0 + (ax1 - ax0) * t
            py = BIG_Y + ay0 + (ay1 - ay0) * t * t
            d.ellipse([px, py, px + 3, py + 3], fill=(255, 220, 130))
burst(x0 + 190, BIG_Y + 66, 13)
burst(x0 + 90, BIG_Y + 78, 11)
burst(x0 + 250, BIG_Y + 60, 9)
banner(x0, BIG_Y, 92, 24, "KYIV", font(SANSB, 16))
banner(x0, BIG_Y + 24, 118, 18, "3 bridges hit", font(SANSB, 11),
       bg=(255, 255, 255), fg=INK)
text(x0 + BIG_W - 6, BIG_Y + BIG_H - 16, "Mayor\u2019s count", font(SANSB, 10),
     fill=(255, 255, 255), anchor="ra")

# --- 2. CYCLONE AKVAN: Bay of Bengal, Odisha coast, spiral
x0 = big_x[1]
d.rectangle([x0, BIG_Y, x0 + BIG_W, BIG_Y + BIG_H], fill=(127, 179, 213))
# land: Odisha / Andhra coast bottom-left
d.polygon([(x0, BIG_Y + 62), (x0 + 95, BIG_Y + 58), (x0 + 130, BIG_Y + 82),
           (x0 + 118, BIG_Y + BIG_H), (x0, BIG_Y + BIG_H)], fill=(232, 214, 165))
d.polygon([(x0 + 95, BIG_Y + 58), (x0 + 150, BIG_Y + 44), (x0 + 175, BIG_Y + 66),
           (x0 + 130, BIG_Y + 82)], fill=(214, 192, 140))
text(x0 + 14, BIG_Y + 70, "ODISHA", font(SANSB, 11), fill=(90, 60, 20))
text(x0 + 14, BIG_Y + 84, "INDIA", font(SANSB, 11), fill=(90, 60, 20))
text(x0 + 130, BIG_Y + 106, "BAY OF BENGAL", font(SANSB, 9), fill=(40, 70, 100))
# spiral: concentric arcs
cx, cy = x0 + 225, BIG_Y + 52
for r in (52, 42, 32, 22, 12):
    d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=4)
d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
# track: dashed red path from Gopalpur to the eye
gx, gy = x0 + 108, BIG_Y + 66
for i in range(13):
    t = i / 12
    px = gx + (cx - gx) * t
    py = gy + (cy - gy) * t - 14 * t * (1 - t) * 4
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=RED)
d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(255, 255, 255))
text(gx + 10, gy + 8, "Gopalpur", font(SANSB, 10), fill=RED)
banner(x0, BIG_Y, 168, 24, "CYCLONE AKVAN", font(SANSB, 16))
banner(x0, BIG_Y + 24, 118, 18, "Landfall \u00b7 8 am", font(SANSB, 11),
       bg=(255, 255, 255), fg=INK)
text(x0 + BIG_W - 6, BIG_Y + BIG_H - 16, "Weather office", font(SANSB, 10),
     fill=(40, 70, 100), anchor="ra")

# --- 3. AI SELL-OFF: dark chart panel with closing values
x0 = big_x[2]
d.rectangle([x0, BIG_Y, x0 + BIG_W, BIG_Y + BIG_H], fill=(16, 24, 40))
for gy in range(BIG_Y + 30, BIG_Y + BIG_H, 24):
    d.line([(x0 + 8, gy), (x0 + 180, gy)], fill=(40, 55, 80), width=1)
pts = [(x0 + 12, BIG_Y + 22), (x0 + 45, BIG_Y + 34), (x0 + 78, BIG_Y + 30),
       (x0 + 105, BIG_Y + 58), (x0 + 135, BIG_Y + 52), (x0 + 165, BIG_Y + 88),
       (x0 + 178, BIG_Y + 100)]
d.line(pts, fill=(230, 60, 60), width=4)
d.polygon([(x0 + 178, BIG_Y + 100), (x0 + 188, BIG_Y + 92), (x0 + 180, BIG_Y + 112)],
          fill=(230, 60, 60))
for (px, py) in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 120, 120))
banner(x0, BIG_Y, 128, 24, "AI SELL-OFF", font(SANSB, 16))
for j, (nm, val) in enumerate([("Taipei", "\u22126.2%"), ("Seoul", "\u22125.2%"),
                               ("Tokyo", "\u22125.1%"), ("SoftBank", "\u221214%")]):
    yy = BIG_Y + 34 + j * 22
    text(x0 + 200, yy, nm, font(SANSB, 12), fill=(255, 255, 255))
    d.text((x0 + 322, yy), val, font=font(SANSB, 12), fill=(255, 90, 90), anchor="ra")

# --- big panel text
big_panel(big_x[0], BIG_Y + BIG_H + 6, BIG_W, "1", "KYIV, UKRAINE \u00b7 WAR",
          "Russian missiles hit three Kyiv bridges",
          "Overnight barrage of 100+ missiles and 400 drones kills 8, injures 28; "
          "power and water cut. (Kyiv Independent, BBC)")
big_panel(big_x[1], BIG_Y + BIG_H + 6, BIG_W, "2", "ODISHA, INDIA \u00b7 CYCLONE",
          "Cyclone Akvan comes ashore in eastern India",
          "Crossed near Gopalpur about 8 am; 300,000+ moved to shelters; winds "
          "70\u201380 km/h; no deaths reported. (IMD, PTI)")
big_panel(big_x[2], BIG_Y + BIG_H + 6, BIG_W, "3",
          "TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS",
          "AI sell-off sinks Asia\u2019s stock markets",
          "Taiwan \u22126.2%, Seoul \u22125.2%, Tokyo \u22125.1% as chipmakers lead the "
          "slide; worst week since 2020. (Al Jazeera, Reuters)")

# ---------------------------------------------------------------- small rows
SM_W, SM_H, SM_GAP = 193, 74, 8
SM_X = [12 + i * (SM_W + SM_GAP) for i in range(5)]
ROW1_Y, ROW2_Y = 438, 604


def union_jack(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(0, 36, 125))
    d.polygon([(x, y), (x + 14, y), (x + w_ - 14, y + h_), (x + w_, y + h_),
               (x + w_, y + h_ - 14), (x, y + 14)], fill=(255, 255, 255))
    d.polygon([(x + w_, y), (x + w_ - 14, y), (x + 14, y + h_), (x, y + h_),
               (x, y + h_ - 14), (x + w_, y + 14)], fill=(255, 255, 255))
    d.rectangle([x + w_ / 2 - 7, y, x + w_ / 2 + 7, y + h_], fill=(255, 255, 255))
    d.rectangle([x, y + h_ / 2 - 7, x + w_, y + h_ / 2 + 7], fill=(255, 255, 255))
    d.rectangle([x + w_ / 2 - 4, y, x + w_ / 2 + 4, y + h_], fill=(200, 16, 46))
    d.rectangle([x, y + h_ / 2 - 4, x + w_, y + h_ / 2 + 4], fill=(200, 16, 46))


def eu_flag(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(0, 51, 153))
    import math
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx = x + w_ / 2 + (w_ / 2 - 12) * math.cos(ang)
        sy = y + h_ / 2 + (h_ / 2 - 10) * math.sin(ang)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))


# --- 4. UK-EU DEAL
x0 = SM_X[0]
union_jack(x0, ROW1_Y, SM_W // 2, SM_H)
eu_flag(x0 + SM_W // 2, ROW1_Y, SM_W - SM_W // 2, SM_H)
banner(x0 + 52, ROW1_Y + SM_H - 20, 90, 18, "AGREED", font(SANSB, 11),
       bg=(255, 255, 255), fg=INK)

# --- 5. COP31: globe + thermometer + NO DEAL
x0 = SM_X[1]
d.rectangle([x0, ROW1_Y, x0 + SM_W, ROW1_Y + SM_H], fill=(178, 216, 228))
d.ellipse([x0 + 12, ROW1_Y + 8, x0 + 72, ROW1_Y + 68], fill=(70, 130, 180))
d.polygon([(x0 + 24, ROW1_Y + 22), (x0 + 44, ROW1_Y + 16), (x0 + 52, ROW1_Y + 30),
           (x0 + 36, ROW1_Y + 38)], fill=(90, 170, 90))
d.polygon([(x0 + 30, ROW1_Y + 44), (x0 + 56, ROW1_Y + 42), (x0 + 60, ROW1_Y + 58),
           (x0 + 40, ROW1_Y + 60)], fill=(90, 170, 90))
d.rectangle([x0 + 150, ROW1_Y + 12, x0 + 160, ROW1_Y + 52], fill=(255, 255, 255),
            outline=INK, width=1)
d.rectangle([x0 + 152, ROW1_Y + 34, x0 + 158, ROW1_Y + 50], fill=RED)
d.ellipse([x0 + 144, ROW1_Y + 48, x0 + 166, ROW1_Y + 68], fill=RED)
banner(x0 + 78, ROW1_Y + 8, 108, 20, "COP31: NO DEAL", font(SANSB, 12))
text(x0 + 80, ROW1_Y + 34, "Final day", font(SANSB, 11), fill=INK)
text(x0 + 80, ROW1_Y + 48, "Antalya", font(SANSB, 11), fill=INK)

# --- 6. POLAND: field, missile, jets
x0 = SM_X[2]
d.rectangle([x0, ROW1_Y, x0 + SM_W, ROW1_Y + SM_H], fill=(168, 205, 141))
d.rectangle([x0, ROW1_Y + 52, x0 + SM_W, ROW1_Y + SM_H], fill=(122, 168, 92))
for fx in range(x0, x0 + SM_W, 16):
    d.line([(fx, ROW1_Y + 52), (fx + 6, ROW1_Y + 40)], fill=(90, 130, 70), width=1)
# missile silhouette
d.polygon([(x0 + 60, ROW1_Y + 26), (x0 + 150, ROW1_Y + 14), (x0 + 150, ROW1_Y + 26),
           (x0 + 60, ROW1_Y + 38)], fill=(80, 80, 80))
d.polygon([(x0 + 150, ROW1_Y + 14), (x0 + 166, ROW1_Y + 20), (x0 + 150, ROW1_Y + 26)],
          fill=(60, 60, 60))
d.polygon([(x0 + 60, ROW1_Y + 26), (x0 + 44, ROW1_Y + 18), (x0 + 44, ROW1_Y + 34)],
          fill=(60, 60, 60))
d.line([(x0 + 44, ROW1_Y + 26), (x0 + 20, ROW1_Y + 30)], fill=(255, 255, 255), width=2)
# dashed border
for i in range(0, SM_W, 12):
    d.line([(x0 + i, ROW1_Y + 58), (x0 + i + 7, ROW1_Y + 58)], fill=RED, width=2)
banner(x0, ROW1_Y, 128, 20, "KH-101 IN POLAND", font(SANSB, 11))

# --- 7. IRAQ: desert convoy
x0 = SM_X[3]
d.rectangle([x0, ROW1_Y, x0 + SM_W, ROW1_Y + SM_H], fill=(238, 214, 160))
d.ellipse([x0 + 150, ROW1_Y + 6, x0 + 178, ROW1_Y + 34], fill=(255, 190, 80))
for tx, tw in [(18, 58), (92, 58)]:
    d.rectangle([x0 + tx, ROW1_Y + 40, x0 + tx + tw, ROW1_Y + 58], fill=(60, 70, 50))
    d.rectangle([x0 + tx + 12, ROW1_Y + 30, x0 + tx + 34, ROW1_Y + 40], fill=(60, 70, 50))
    d.line([(x0 + tx + 34, ROW1_Y + 33), (x0 + tx + 58, ROW1_Y + 28)],
           fill=(60, 70, 50), width=3)
    for wx in range(tx + 4, tx + tw - 6, 12):
        d.ellipse([x0 + wx, ROW1_Y + 60, x0 + wx + 8, ROW1_Y + 68], fill=(40, 40, 40))
d.line([(x0 + 168, ROW1_Y + 58), (x0 + 168, ROW1_Y + 34)], fill=(120, 80, 40), width=3)
for a in (-50, -20, 10, 40):
    import math
    d.line([(x0 + 168, ROW1_Y + 34),
            (x0 + 168 + 16 * math.cos(math.radians(a - 90)),
             ROW1_Y + 34 + 16 * math.sin(math.radians(a - 90)))],
           fill=(60, 120, 60), width=2)
banner(x0, ROW1_Y, 74, 20, "ARMY IN", font(SANSB, 11))

# --- 8. ITALY: strike crowd
x0 = SM_X[4]
d.rectangle([x0, ROW1_Y, x0 + SM_W, ROW1_Y + SM_H], fill=(240, 235, 220))
d.rectangle([x0, ROW1_Y, x0 + SM_W // 3, ROW1_Y + 10], fill=(0, 146, 70))
d.rectangle([x0 + SM_W // 3, ROW1_Y, x0 + 2 * SM_W // 3, ROW1_Y + 10],
            fill=(255, 255, 255))
d.rectangle([x0 + 2 * SM_W // 3, ROW1_Y, x0 + SM_W, ROW1_Y + 10], fill=(205, 0, 40))
for i, px in enumerate(range(x0 + 12, x0 + SM_W - 10, 24)):
    d.ellipse([px, ROW1_Y + 26, px + 12, ROW1_Y + 38], fill=(50, 50, 50))
    d.rectangle([px - 3, ROW1_Y + 40, px + 15, ROW1_Y + 58], fill=(50, 50, 50))
    if i % 2 == 0:
        d.rectangle([px - 8, ROW1_Y + 14, px + 20, ROW1_Y + 24], fill=(255, 255, 255),
                    outline=INK, width=1)
banner(x0 + 46, ROW1_Y + SM_H - 20, 100, 18, "SCIOPERO", font(SANSB, 11),
       bg=(255, 255, 255), fg=INK)

# --- row 1 text
small_panel(SM_X[0], ROW1_Y + SM_H + 6, SM_W, "4", "BRUSSELS \u00b7 DIPLOMACY",
            "UK and EU seal a \u2018reset\u2019 deal",
            "Food trade, youth visas, carbon link. (Reuters)")
small_panel(SM_X[1], ROW1_Y + SM_H + 6, SM_W, "5", "ANTALYA \u00b7 CLIMATE",
            "COP31 reaches its last day with no deal",
            "Draft leaves out fossil fuels; $120bn adaptation dropped. (UN News)")
small_panel(SM_X[2], ROW1_Y + SM_H + 6, SM_W, "6", "LUBLIN \u00b7 SECURITY",
            "Russian cruise missile lands in Poland",
            "Fell in a field; jets scrambled; Warsaw protests. (Reuters)")
small_panel(SM_X[3], ROW1_Y + SM_H + 6, SM_W, "7", "JURF AL-SAKHAR \u00b7 SECURITY",
            "Iraqi army enters a militia stronghold",
            "Troops deploy to Jurf al-Sakhar. (Reuters)")
small_panel(SM_X[4], ROW1_Y + SM_H + 6, SM_W, "8", "ROME \u00b7 LABOUR",
            "General strike over Italy\u2019s budget",
            "Workers and students march in 100 squares. (Reuters)")

# --- 9. JAPAN: red sun + rising bars
x0 = SM_X[0]
d.rectangle([x0, ROW2_Y, x0 + SM_W, ROW2_Y + SM_H], fill=(255, 255, 255))
d.ellipse([x0 + 14, ROW2_Y + 12, x0 + 58, ROW2_Y + 56], fill=(188, 0, 45))
for i, bh in enumerate((14, 24, 34, 46)):
    d.rectangle([x0 + 76 + i * 28, ROW2_Y + SM_H - 12 - bh,
                 x0 + 76 + i * 28 + 20, ROW2_Y + SM_H - 12], fill=RED)
banner(x0 + 118, ROW2_Y + 4, 70, 20, "2.3%", font(SANSB, 13))

# --- 10. SEOUL: parliament + gavel
x0 = SM_X[1]
d.rectangle([x0, ROW2_Y, x0 + SM_W, ROW2_Y + SM_H], fill=(214, 228, 240))
d.polygon([(x0 + 60, ROW2_Y + 14), (x0 + 133, ROW2_Y + 14), (x0 + 122, ROW2_Y + 24),
           (x0 + 71, ROW2_Y + 24)], fill=(90, 90, 90))
d.rectangle([x0 + 66, ROW2_Y + 24, x0 + 127, ROW2_Y + 30], fill=(70, 70, 70))
for cx in range(x0 + 72, x0 + 128, 12):
    d.rectangle([cx, ROW2_Y + 30, cx + 5, ROW2_Y + 58], fill=(110, 110, 110))
d.rectangle([x0 + 62, ROW2_Y + 58, x0 + 131, ROW2_Y + 64], fill=(70, 70, 70))
d.line([(x0 + 150, ROW2_Y + 20), (x0 + 178, ROW2_Y + 48)], fill=(120, 80, 40), width=4)
d.rectangle([x0 + 144, ROW2_Y + 12, x0 + 162, ROW2_Y + 26], fill=(120, 80, 40))
banner(x0, ROW2_Y, 86, 20, "IMPEACH", font(SANSB, 11))

# --- 11. KENYA: oil derrick at sunset
x0 = SM_X[2]
d.rectangle([x0, ROW2_Y, x0 + SM_W, ROW2_Y + SM_H], fill=(250, 180, 90))
d.ellipse([x0 + 140, ROW2_Y + 8, x0 + 172, ROW2_Y + 40], fill=(255, 220, 120))
d.polygon([(x0 + 78, ROW2_Y + 62), (x0 + 96, ROW2_Y + 10), (x0 + 114, ROW2_Y + 62)],
          fill=(40, 40, 40))
d.line([(x0 + 96, ROW2_Y + 10), (x0 + 96, ROW2_Y + 62)], fill=(20, 20, 20), width=2)
d.line([(x0 + 84, ROW2_Y + 44), (x0 + 108, ROW2_Y + 44)], fill=(20, 20, 20), width=2)
d.rectangle([x0, ROW2_Y + 62, x0 + SM_W, ROW2_Y + SM_H], fill=(120, 70, 30))
banner(x0, ROW2_Y, 92, 20, "FIRST OIL", font(SANSB, 11))

# --- 12. BUKELE: ballot box
x0 = SM_X[3]
d.rectangle([x0, ROW2_Y, x0 + SM_W, ROW2_Y + SM_H], fill=(36, 80, 164))
d.rectangle([x0 + 58, ROW2_Y + 30, x0 + 138, ROW2_Y + 66], fill=(255, 255, 255),
            outline=(20, 40, 90), width=2)
d.rectangle([x0 + 84, ROW2_Y + 36, x0 + 112, ROW2_Y + 42], fill=(20, 40, 90))
d.polygon([(x0 + 92, ROW2_Y + 8), (x0 + 128, ROW2_Y + 14), (x0 + 122, ROW2_Y + 34),
           (x0 + 86, ROW2_Y + 28)], fill=(255, 255, 255), outline=INK)
text(x0 + 107, ROW2_Y + 12, "\u2713", font(SANSB, 14), fill=RED, anchor="mm")
banner(x0 + 96, ROW2_Y + 48, 92, 20, "3RD TERM", font(SANSB, 11))

# --- 13. PHILLIPS: cricket
x0 = SM_X[4]
d.rectangle([x0, ROW2_Y, x0 + SM_W, ROW2_Y + SM_H], fill=(120, 180, 100))
d.rectangle([x0 + 60, ROW2_Y + 8, x0 + 133, ROW2_Y + 66], fill=(220, 200, 150))
d.line([(x0 + 78, ROW2_Y + 16), (x0 + 96, ROW2_Y + 52)], fill=(150, 105, 50), width=7)
d.ellipse([x0 + 128, ROW2_Y + 52, x0 + 142, ROW2_Y + 66], fill=(188, 0, 45))
for sx in (x0 + 150, x0 + 156, x0 + 162):
    d.line([(sx, ROW2_Y + 18), (sx, ROW2_Y + 34)], fill=(255, 255, 255), width=2)
text(x0 + 14, ROW2_Y + 8, "118", font(SERIFB, 30), fill=(255, 255, 255))

# --- row 2 text
small_panel(SM_X[0], ROW2_Y + SM_H + 6, SM_W, "9", "TOKYO \u00b7 ECONOMY",
            "Japan\u2019s inflation picks up to 2.3%",
            "December rate rise stays in view. (Official data)")
small_panel(SM_X[1], ROW2_Y + SM_H + 6, SM_W, "10", "SEOUL \u00b7 POLITICS",
            "Korea\u2019s ruling party to impeach top judge",
            "Follows an overturned conviction. (Korea Herald)")
small_panel(SM_X[2], ROW2_Y + SM_H + 6, SM_W, "11", "TURKANA \u00b7 ENERGY",
            "Kenya starts drilling its first oil well",
            "First crude due on 1 December. (allAfrica)")
small_panel(SM_X[3], ROW2_Y + SM_H + 6, SM_W, "12", "SAN SALVADOR \u00b7 POLITICS",
            "Bukele files to run for a third term",
            "The vote is on 28 February 2027. (AP)")
small_panel(SM_X[4], ROW2_Y + SM_H + 6, SM_W, "13", "WELLINGTON \u00b7 CRICKET",
            "Phillips hits 118 against India",
            "Hundreds in all three formats. (ICC)")

# ---------------------------------------------------------------- map + briefs
MAP_X, MAP_Y, MAP_W, MAP_H = 12, 786, 288, 172
text(12, 764, "WHERE IT HAPPENED", font(SANSB, 13), fill=RED)
text(312, 764, "ALSO ON FRIDAY 20 NOVEMBER \u2014 22 MORE STORIES",
     font(SANSB, 13))
hline(782, x1=1012, wdt=1)

d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA)


def mx(lon):
    return MAP_X + (lon + 168) / 360 * MAP_W


def my(lat):
    return MAP_Y + (78 - lat) / 136 * MAP_H


CONTINENTS = [
    # North America
    [(-165, 65), (-150, 70), (-130, 71), (-110, 72), (-95, 75), (-85, 70),
     (-75, 62), (-70, 45), (-75, 35), (-80, 26), (-85, 20), (-90, 15),
     (-95, 17), (-105, 20), (-112, 28), (-120, 35), (-125, 45), (-125, 50),
     (-140, 60), (-155, 58), (-165, 65)],
    # South America
    [(-80, 10), (-60, 5), (-50, -5), (-40, -20), (-48, -28), (-58, -35),
     (-65, -45), (-70, -52), (-73, -40), (-75, -20), (-80, -5), (-80, 10)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 10), (48, 0), (40, -10), (35, -20), (32, -28), (26, -33),
     (18, -35), (12, -18), (9, 4), (-8, 5), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (60, 70), (90, 75),
     (120, 73), (150, 70), (178, 66), (170, 60), (162, 56), (158, 52),
     (142, 45), (140, 38), (130, 33), (127, 35), (122, 30), (120, 22),
     (110, 20), (105, 10), (100, 8), (97, 16), (92, 21), (89, 22), (86, 20),
     (80, 15), (76, 10), (72, 20), (66, 25), (60, 25), (55, 26), (50, 29),
     (48, 30), (43, 35), (40, 36), (36, 36), (30, 36), (30, 42), (28, 45),
     (30, 50), (28, 55), (20, 54), (12, 54), (8, 57), (5, 58), (-5, 58),
     (-10, 54), (-10, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (142, -38), (147, -39), (150, -37), (153, -32), (153, -27), (146, -19),
     (142, -11), (137, -12), (135, -15), (132, -12), (126, -14), (122, -17),
     (118, -20), (113, -22)],
]
for poly in CONTINENTS:
    d.polygon([(mx(lo), my(la)) for lo, la in poly], fill=LAND)

PINS = [
    (1, 30.5, 50.5, 7, 0), (2, 84.9, 19.3, 0, 0), (3, 121.5, 25.0, 0, 0),
    (4, 4.35, 50.85, -9, 3), (5, 30.7, 36.9, -14, 12), (6, 22.6, 51.25, -7, -7),
    (7, 44.2, 32.8, 0, 0), (8, 12.5, 41.9, -5, 9), (9, 139.7, 35.7, 8, 8),
    (10, 127.0, 37.5, -10, -6), (11, 36.0, 3.5, 0, 0), (12, -89.2, 13.7, 0, 0),
    (13, 174.8, -41.3, -4, -4),
]
for num, lon, lat, dx, dy in PINS:
    cx, cy = mx(lon) + dx, my(lat) + dy
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=font(SANSB, 9), fill=(255, 255, 255),
           anchor="mm")

BRIEFS = [
    (14, "Lviv", "Rail station strike kills two (BBC)"),
    (15, "US\u2013Venezuela", "Deal restores military ties (AP)"),
    (16, "Senate", "Iran war-powers bid fails 51\u201348"),
    (17, "Pete Rose", "Trump pardons the late legend"),
    (18, "UK drones", "1,000+ drones for Ukraine, \u00a3260m"),
    (19, "E3", "Leaders call for a winter energy ceasefire"),
    (20, "Nvidia", "California probes its China chip sales"),
    (21, "Cancer pill", "Tumours shrink in 60.7% of patients"),
    (22, "BepiColombo", "Probe reaches Mercury after 8 years"),
    (23, "Hormuz", "Tanker ablaze off Oman; no casualties"),
    (24, "Anthropic", "Shares fall on day two after debut"),
    (25, "Rohingya", "Camps react to Thursday\u2019s ICJ ruling"),
    (26, "Shenzhen", "Three leaders issue a peace declaration"),
    (27, "Moscow", "Estonia\u2019s border crossing to shut"),
    (28, "Berlin", "Pupils strike over military service"),
    (29, "Beijing", "Loan rates held for an 18th month"),
    (30, "Seoul", "KOSPI ends the week 7.9% lower"),
    (31, "Ganjam", "209 mm of rain as Akvan crosses Odisha"),
    (32, "Lebanon", "Israeli jets strike south and east"),
    (33, "Malawi", "Fuel crisis brings all-night queues"),
    (34, "Abuja", "Court bars new evidence vs Tinubu"),
    (35, "Sydney", "Shares fall 1.8% in the sell-off"),
]
for i, (num, place, txt) in enumerate(BRIEFS):
    col = 0 if i < 11 else 1
    row = i % 11
    bx = 312 + col * 356
    by = MAP_Y + row * 15.6
    text(bx, by, f"{num}", font(SANSB, 11), fill=RED)
    n_w = d.textlength(f"{num} ", font=font(SANSB, 11))
    text(bx + n_w, by, f"{place} \u2014 {txt}", font(SANS, 11))

text(12, 962, "Red numbers mark stories 1\u201313.", font(SANS, 10), fill=GREY)
text(1012, 962, "Sources named beside each story \u00b7 original drawings",
     font(SANS, 10), fill=GREY, anchor="ra")

# ---------------------------------------------------------------- date check
d.rectangle([12, 984, 1012, 1020], outline=RED, width=2)
dc = ("DATE CHECK \u2014 Left out on purpose: the Shenzhen summit itself met on "
      "Thursday 19 Nov \u2014 Friday\u2019s news is the declaration and the missiles "
      "that followed. The ICJ\u2019s Myanmar ruling and Anthropic\u2019s $83 debut were "
      "Thursday; Friday\u2019s news is the reaction and the second day. Not yet: "
      "COP31\u2019s final text; BepiColombo\u2019s Mercury orbit entry.")
for j, ln in enumerate(wrap(dc, font(SANS, 11), 984)):
    text(22, 986 + j * 13, ln, font(SANS, 11))

img.save("entry.png")
print("saved entry.png", img.size)
