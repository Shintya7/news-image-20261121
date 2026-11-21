#!/usr/bin/env python3
"""Draw entry.png for news-image-20261121: a newspaper front page summing up
Saturday 21 November 2026 world news. Six story panels (3x2), each with a flat
drawn illustration, a headline and one factual sub-line. No photos, no logos.
Run: python3 draw.py  (writes entry.png beside this file, 1024x1024)."""

from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (27, 42, 74)
GOLD = (232, 182, 76)
INK = (24, 24, 24)
MUTED = (90, 88, 80)
PANEL_BG = (255, 255, 255)
BORDER = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
F_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
F_REG = FONT_DIR + "NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt_path, size, max_w, max_lines):
    """Shrink font until text fits in max_lines at max_w. Returns (font, lines)."""
    while size > 10:
        fnt = font(fnt_path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(fnt_path, size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def panel(draw, x, y, w, h, tag, tag_color):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=BORDER, width=2)
    return x, y, w, h


def tag_chip(draw, x, y, text, color):
    fnt = font(F_BOLD, 15)
    tw = draw.textlength(text, font=fnt)
    pad = 8
    draw.rectangle([x, y, x + tw + pad * 2, y + 22], fill=color)
    draw.text((x + pad, y + 3), text, font=fnt, fill=(255, 255, 255))


def draw_poland(d, x, y, w, h):
    # Night sky, two missile streaks, border ground, Polish flag
    d.rectangle([x, y, x + w, y + h], fill=(38, 52, 84))
    for sx, sy in [(40, 30), (120, 60), (210, 24), (260, 70), (90, 100)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 255, 255))
    # missile 1: streak + flame
    d.line([x + 30, y + 150, x + 150, y + 70], fill=(232, 182, 76), width=6)
    d.line([x + 34, y + 154, x + 154, y + 74], fill=(255, 240, 200), width=2)
    d.polygon([(x + 150, y + 70), (x + 168, y + 78), (x + 154, y + 88)],
              fill=(200, 60, 40))
    # missile 2
    d.line([x + 120, y + 168, x + 250, y + 96], fill=(232, 182, 76), width=6)
    d.polygon([(x + 250, y + 96), (x + 268, y + 104), (x + 254, y + 114)],
              fill=(200, 60, 40))
    # ground
    d.rectangle([x, y + h - 40, x + w, y + h], fill=(70, 90, 60))
    # flag pole + Polish flag (white over red)
    d.line([x + 44, y + h - 40, x + 44, y + h - 118], fill=(220, 220, 220), width=4)
    d.rectangle([x + 44, y + h - 118, x + 104, y + h - 98], fill=(255, 255, 255))
    d.rectangle([x + 44, y + h - 98, x + 104, y + h - 78], fill=(200, 40, 50))
    # NATO stars ring, small
    cx, cy = x + w - 52, y + h - 66
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        sx = cx + int(16 * math.cos(a))
        sy = cy + int(16 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def draw_markets(d, x, y, w, h):
    # Chart: grey bars, red line plunging, red arrowhead
    d.rectangle([x, y, x + w, y + h], fill=(238, 238, 236))
    for i in range(8):
        bx = x + 22 + i * 36
        bh = 40 + i * 12
        d.rectangle([bx, y + h - 46 - bh, bx + 20, y + h - 46],
                    fill=(170, 175, 180))
    pts = [(x + 28, y + 34), (x + 70, y + 52), (x + 112, y + 48),
           (x + 154, y + 84), (x + 196, y + 96), (x + 238, y + 138),
           (x + 282, y + 168)]
    d.line(pts, fill=(196, 40, 40), width=6, joint="curve")
    d.polygon([(x + 282, y + 168), (x + 296, y + 150), (x + 300, y + 172)],
              fill=(196, 40, 40))
    fnt = font(F_BOLD, 26)
    d.text((x + w - 92, y + 12), "-3.7%", font=fnt, fill=(196, 40, 40))
    d.rectangle([x, y + h - 46, x + w, y + h - 42], fill=(120, 120, 120))


def draw_peace(d, x, y, w, h):
    # Calendar page marked JANUARY + olive branch + handshake bars
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    # calendar
    cx, cy = x + 58, y + 30
    d.rectangle([cx, cy, cx + 190, cy + 120], fill=(255, 255, 255),
                outline=NAVY, width=3)
    d.rectangle([cx, cy, cx + 190, cy + 32], fill=NAVY)
    fnt = font(F_BOLD, 20)
    d.text((cx + 52, cy + 5), "JANUARY", font=fnt, fill=(255, 255, 255))
    fnt2 = font(F_BOLD, 34)
    d.text((cx + 66, cy + 52), "2027", font=fnt2, fill=NAVY)
    # olive branch, clear of the calendar
    bx, by = x + 40, y + 172
    d.line([bx, by, bx + 220, by - 10], fill=(46, 140, 90), width=4)
    for i in range(5):
        lx = bx + 12 + i * 42
        ly = by - 2 - i * 2
        d.ellipse([lx, ly - 14, lx + 34, ly + 4], fill=(46, 140, 90))
        d.line([lx + 4, ly + 2, lx + 30, ly - 12], fill=(255, 255, 255), width=2)


def draw_kryvyi(d, x, y, w, h):
    # Apartment block with broken windows, smoke, ambulance with red cross
    d.rectangle([x, y, x + w, y + h], fill=(226, 216, 196))
    for i, r in enumerate([24, 18, 13]):
        d.ellipse([x + 210 + i * 10, y + 10 + i * 14, x + 210 + i * 10 + r * 2,
                   y + 10 + i * 14 + r * 2], fill=(160, 160, 160))
    bx, by = x + 40, y + 40
    d.rectangle([bx, by, bx + 180, y + h - 52], fill=(190, 170, 140),
                outline=(90, 80, 60), width=3)
    for row in range(3):
        for col in range(3):
            wx = bx + 18 + col * 56
            wy = by + 20 + row * 40
            d.rectangle([wx, wy, wx + 34, wy + 26], fill=(240, 230, 200),
                        outline=(90, 80, 60), width=2)
            if (row, col) in [(0, 1), (1, 0)]:
                d.line([wx, wy, wx + 34, wy + 26], fill=(60, 50, 40), width=2)
                d.line([wx + 34, wy, wx, wy + 26], fill=(60, 50, 40), width=2)
    # ambulance
    ax, ay = x + 176, y + h - 48
    d.rectangle([ax, ay, ax + 108, ay + 34], fill=(255, 255, 255),
                outline=(196, 40, 40), width=3)
    d.rectangle([ax + 42, ay + 6, ax + 54, ay + 28], fill=(196, 40, 40))
    d.rectangle([ax + 36, ay + 12, ax + 60, ay + 22], fill=(196, 40, 40))
    d.ellipse([ax + 12, ay + 30, ax + 28, ay + 44], fill=(40, 40, 40))
    d.ellipse([ax + 76, ay + 30, ax + 92, ay + 44], fill=(40, 40, 40))


def draw_unsc(d, x, y, w, h):
    # UN blue: emblem circle + horseshoe council table + flags
    d.rectangle([x, y, x + w, y + h], fill=(200, 218, 238))
    cx, cy = x + w // 2, y + 62
    d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=(30, 90, 170))
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(200, 218, 238))
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(30, 90, 170))
    # horseshoe table
    d.arc([x + 30, y + 96, x + w - 30, y + h + 40], start=180, end=360,
          fill=(120, 90, 60), width=16)
    # seats: small flags around the arc
    flag_cols = [(30, 60, 160), (200, 40, 50), (255, 255, 255),
                 (46, 140, 90), (232, 182, 76)]
    for i, c in enumerate(flag_cols):
        ang = math.radians(200 + i * 35)
        fx = x + w // 2 + int(118 * math.cos(ang))
        fy = y + 148 + int(52 * math.sin(ang))
        d.rectangle([fx - 12, fy - 10, fx + 12, fy + 10], fill=c,
                    outline=(90, 80, 60), width=2)
    # gavel
    d.line([x + 130, y + h - 26, x + 176, y + h - 52], fill=(90, 70, 50), width=5)
    d.rectangle([x + 164, y + h - 62, x + 196, y + h - 46], fill=(120, 90, 60))


def draw_estonia(d, x, y, w, h):
    # Road, striped barrier arm, signpost, pine trees, two flag bars
    d.rectangle([x, y, x + w, y + h], fill=(206, 226, 208))
    d.rectangle([x, y + h - 56, x + w, y + h], fill=(110, 110, 108))
    d.line([x, y + h - 28, x + w, y + h - 28], fill=(255, 255, 255), width=4)
    # pine trees
    for tx in (36, 262):
        d.polygon([(x + tx, y + 26), (x + tx + 22, y + 78),
                   (x + tx + 44, y + 26)], fill=(46, 110, 70))
        d.polygon([(x + tx + 6, y + 52), (x + tx + 22, y + 96),
                   (x + tx + 38, y + 52)], fill=(46, 110, 70))
        d.rectangle([x + tx + 18, y + 96, x + tx + 26, y + 118],
                    fill=(90, 70, 50))
    # barrier post + striped arm
    d.rectangle([x + 96, y + 84, x + 108, y + h - 56], fill=(200, 40, 50))
    for i in range(5):
        col = (255, 255, 255) if i % 2 == 0 else (200, 40, 50)
        d.rectangle([x + 108 + i * 36, y + 84, x + 108 + (i + 1) * 36, y + 100],
                    fill=col, outline=(120, 120, 120), width=1)
    # signpost
    d.line([x + 226, y + 108, x + 226, y + h - 56], fill=(90, 80, 60), width=4)
    d.rectangle([x + 196, y + 108, x + 256, y + 132], fill=(255, 255, 255),
                outline=NAVY, width=2)
    fnt = font(F_BOLD, 13)
    d.text((x + 202, y + 114), "CLOSED", font=fnt, fill=(196, 40, 40))
    # flag bars: Estonia (blue/black/white) and Russia (white/blue/red)
    for j, cols in enumerate([[(30, 90, 170), (30, 30, 30), (255, 255, 255)],
                             [(255, 255, 255), (30, 60, 160), (200, 40, 50)]]):
        fx = x + 118 + j * 84
        for k, c in enumerate(cols):
            d.rectangle([fx, y + h - 48 + k * 8, fx + 64, y + h - 40 + k * 8],
                        fill=c)


STORIES = [
    dict(tag="NATO", color=(27, 42, 74),
         draw=draw_poland,
         headline="RUSSIAN MISSILES LAND IN POLAND",
         sub="Tusk calls it a deliberate provocation; NATO's Rutte: 'grave violation'"),
    dict(tag="MARKETS", color=(196, 40, 40),
         draw=draw_markets,
         headline="WALL STREET PLUNGES INTO CORRECTION",
         sub="S&P 500 -3.7%, Nasdaq -5.3%; Nvidia falls 14% on SEC probe report"),
    dict(tag="DIPLOMACY", color=(30, 60, 160),
         draw=draw_peace,
         headline="TRUMP WANTS UKRAINE DEAL BY JANUARY",
         sub="FT: White House presses Kyiv and Moscow; 'Americans in a hurry, Putin in no hurry'"),
    dict(tag="UKRAINE", color=(120, 60, 50),
         draw=draw_kryvyi,
         headline="MISSILES KILL TWO IN KRYVYI RIH",
         sub="Boy, 7, and a paramedic, 20, dead; 42 hurt as drones hit rescuers"),
    dict(tag="UNITED NATIONS", color=(30, 90, 170),
         draw=draw_unsc,
         headline="FRANCE SEEKS UN SECURITY COUNCIL MEETING",
         sub="Paris acts after Kyiv strikes kill eight and damage two embassies"),
    dict(tag="BALTICS", color=(46, 110, 70),
         draw=draw_estonia,
         headline="ESTONIA SHUTS ITS BORDER WITH RUSSIA",
         sub="Road crossings close from 1 Dec for six months after alleged GRU arson plot"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    f_mast = font(F_BOLD, 62)
    mast = "THE WORLD TODAY"
    tw = d.textlength(mast, font=f_mast)
    d.text(((W - tw) / 2, 12), mast, font=f_mast, fill=(255, 255, 255))
    f_date = font(F_BOLD, 34)
    date = "SATURDAY, 21 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 88), date, font=f_date, fill=GOLD)
    f_sub = font(F_REG, 18)
    tagline = "One day in the world  •  Six stories"
    tw = d.textlength(tagline, font=f_sub)
    d.text(((W - tw) / 2, 126), tagline, font=f_sub, fill=(200, 205, 220))

    # Grid of panels: 3 columns x 2 rows
    px = [12, 349, 686]
    py = [160, 572]
    pw, ph = 326, 400
    ill_h = 196
    for i, s in enumerate(STORIES):
        x = px[i % 3]
        y = py[i // 3]
        panel(d, x, y, pw, ph, s["tag"], s["color"])
        s["draw"](d, x + 8, y + 8, pw - 16, ill_h)
        tag_chip(d, x + 8, y + 8, s["tag"], s["color"])
        # headline
        hfnt, hlines = fit_text(d, s["headline"], F_BOLD, 27, pw - 24, 2)
        hy = y + 8 + ill_h + 14
        for line in hlines:
            d.text((x + 12, hy), line, font=hfnt, fill=INK)
            hy += hfnt.size + 4
        # sub-line
        sfnt, slines = fit_text(d, s["sub"], F_REG, 19, pw - 24, 2)
        sy = y + ph - 14 - len(slines) * (sfnt.size + 3)
        for line in slines:
            d.text((x + 12, sy), line, font=sfnt, fill=MUTED)
            sy += sfnt.size + 3

    # Footer ticker
    d.rectangle([0, 980, W, H], fill=NAVY)
    tick = ("ALSO TODAY:  Rutte due in Warsaw  •  Sweden summons Russia's envoy  •  "
            "Gold at a 14-month low  •  Bitcoin below $60,000")
    f_tick = font(F_REG, 17)
    while d.textlength(tick, font=f_tick) > W - 16 and f_tick.size > 10:
        f_tick = font(F_REG, f_tick.size - 1)
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, 995), tick, font=f_tick, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
