#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Thursday 19 November 2026.

Pure PIL, no network, no timestamps, no randomness: running this script
twice produces byte-identical output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

PAPER = (248, 241, 222)
INK = (18, 18, 18)
RED = (163, 29, 33)
GREY = (90, 86, 76)
NAVY = (31, 58, 95)
SKY = (198, 220, 235)
LIGHT = (238, 232, 214)
GREEN = (28, 120, 66)
ORANGE = (232, 122, 48)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, max_w, fill=INK, leading=1.28):
    """Draw wrapped text; returns the y just below the last line."""
    size = fnt.size
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def centred(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def box(draw, x0, y0, x1, y1, width=2):
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=width)


def kicker(draw, x, y, text, size=17):
    draw.text((x, y), text, font=font(SANS_B, size), fill=RED)


def headline(draw, x, y, text, size, max_w, leading=1.08):
    return text_block(draw, x, y, text, font(SERIF_B, size), max_w,
                      leading=leading)


# ---------------------------------------------------------------- figures
def draw_flags_scene(draw, x0, y0, x1, y1):
    """Shenzhen skyline with the US, Chinese and Russian flags."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    base = y1 - 26
    # skyline bars
    heights = [52, 78, 44, 92, 60, 84, 48, 70, 58]
    n = len(heights)
    bw = (x1 - x0) / n
    for i, h in enumerate(heights):
        bx = x0 + i * bw
        draw.rectangle([bx + 2, base - h, bx + bw - 2, base],
                       fill=(96, 96, 96))
        draw.rectangle([bx + bw / 2 - 2, base - h - 12, bx + bw / 2 + 2,
                        base - h], fill=(96, 96, 96))
    # flag poles and flags
    pole_top = y0 + 14
    for i, kind in enumerate(("us", "cn", "ru")):
        px = x0 + 46 + i * 100
        draw.line([(px, pole_top), (px, base)], fill=INK, width=3)
        fx, fy, fw, fh = px + 3, pole_top, 62, 38
        if kind == "us":
            for s in range(7):
                col = (178, 34, 52) if s % 2 == 0 else (255, 255, 255)
                draw.rectangle([fx, fy + s * fh / 7, fx + fw,
                                fy + (s + 1) * fh / 7], fill=col)
            draw.rectangle([fx, fy, fx + 26, fy + 20], fill=(40, 60, 120))
            for dy in (5, 13):
                for dx in (5, 13, 21):
                    draw.ellipse([fx + dx - 1, fy + dy - 1, fx + dx + 1,
                                  fy + dy + 1], fill=(255, 255, 255))
        elif kind == "cn":
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            for dx, dy in ((10, 8), (22, 12), (26, 22), (14, 24)):
                draw.ellipse([fx + dx - 3, fy + dy - 3, fx + dx + 3,
                              fy + dy + 3], fill=(255, 222, 0))
        else:
            for s, col in enumerate(((255, 255, 255), (0, 57, 166),
                                     (213, 0, 50))):
                draw.rectangle([fx, fy + s * fh / 3, fx + fw,
                                fy + (s + 1) * fh / 3], fill=col)
    draw.rectangle([x0, base, x1, y1], fill=NAVY)
    draw.text((x0 + 10, base + 3), "SHENZHEN  •  APEC",
              font=font(SANS_B, 15), fill=(255, 255, 255))


def draw_game_case(draw, x0, y0, x1, y1):
    """Stylised GTA VI game case with an orange sunset disc."""
    draw.rectangle([x0, y0, x1, y1], fill=(24, 24, 46))
    draw.text((x0 + 8, y0 + 5), "GTA VI", font=font(SANS_B, 22),
              fill=(255, 170, 60))
    draw.ellipse([x1 - 34, y0 + 28, x1 - 8, y0 + 54], fill=ORANGE)
    draw.rectangle([x0, y0 + 48, x1, y1 - 16], fill=(255, 178, 102))
    draw.text((x0 + 12, y0 + 50), "VI", font=font(SERIF_B, 26),
              fill=(24, 24, 46))
    draw.rectangle([x0, y1 - 16, x1, y1], fill=RED)
    draw.text((x0 + 8, y1 - 14), "NO PC AT LAUNCH",
              font=font(SANS_B, 11), fill=(255, 255, 255))


def draw_chart(draw, x0, y0, x1, y1):
    """Rising bars and arrow for the record IPO."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 244, 234))
    bars = [16, 26, 22, 38, 52]
    bw = (x1 - x0 - 20) / len(bars)
    base = y1 - 26
    for i, h in enumerate(bars):
        bx = x0 + 10 + i * bw
        draw.rectangle([bx + 3, base - h, bx + bw - 3, base], fill=GREEN)
    draw.line([(x0 + 12, base - 12), (x1 - 12, y0 + 10)], fill=GREEN,
              width=4)
    draw.polygon([(x1 - 12, y0 + 10), (x1 - 28, y0 + 12), (x1 - 14, y0 + 26)],
                 fill=GREEN)
    draw.text((x0 + 8, y1 - 22), "NASDAQ", font=font(SANS_B, 13), fill=GREY)


def draw_bridge(draw, x0, y0, x1, y1):
    """Kerch Bridge with a broken middle span over the strait."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 230, 240))
    mid = (x0 + x1) / 2
    deck_y = y0 + 30
    draw.rectangle([x0, deck_y, mid - 24, deck_y + 9], fill=(60, 60, 60))
    draw.rectangle([mid + 24, deck_y, x1, deck_y + 9], fill=(60, 60, 60))
    draw.polygon([(mid - 24, deck_y + 9), (mid - 8, deck_y + 30),
                  (mid + 4, deck_y + 30), (mid - 12, deck_y + 9)],
                 fill=(60, 60, 60))
    draw.polygon([(mid + 24, deck_y + 9), (mid + 8, deck_y + 30),
                  (mid - 4, deck_y + 30), (mid + 12, deck_y + 9)],
                 fill=(60, 60, 60))
    for wy in (y1 - 30, y1 - 22):
        for wx in range(x0 + 6, x1 - 6, 24):
            draw.arc([wx, wy - 4, wx + 20, wy + 4], 0, 180,
                     fill=(40, 90, 150), width=2)
    draw.rectangle([x0, y1 - 18, x1, y1], fill=(40, 90, 150))
    draw.text((x0 + 8, y1 - 16), "KERCH STRAIT",
              font=font(SANS_B, 12), fill=(255, 255, 255))


def draw_tanker(draw, x0, y0, x1, y1):
    """Oil tanker under a dark blast star in the Strait of Hormuz."""
    draw.rectangle([x0, y0, x1, y1], fill=(238, 228, 200))
    cx = (x0 + x1) / 2
    cy = y0 + 22
    spikes = [(0, -18), (5, -5), (18, 0), (5, 5), (0, 18), (-5, 5),
              (-18, 0), (-5, -5)]
    pts = [(cx + dx, cy + dy) for dx, dy in spikes]
    draw.polygon(pts, fill=(30, 30, 30))
    hull_y = y0 + 52
    draw.polygon([(x0 + 8, hull_y), (x1 - 8, hull_y), (x1 - 26, y1 - 18),
                  (x0 + 26, y1 - 18)], fill=(52, 52, 52))
    draw.rectangle([x0 + 34, hull_y - 14, x0 + 62, hull_y],
                   fill=(150, 100, 40))
    draw.rectangle([x1 - 62, hull_y - 11, x1 - 34, hull_y],
                   fill=(150, 100, 40))
    draw.rectangle([x0, y1 - 18, x1, y1], fill=(40, 90, 150))
    draw.text((x0 + 8, y1 - 16), "HORMUZ", font=font(SANS_B, 12),
              fill=(255, 255, 255))


def draw_court(draw, x0, y0, x1, y1):
    """Courthouse pediment, columns and scales for The Hague."""
    draw.rectangle([x0, y0, x1, y1], fill=(232, 236, 242))
    cx = (x0 + x1) / 2
    h = y1 - y0
    draw.polygon([(x0 + 10, y0 + int(h * 0.30)), (cx, y0 + 4),
                  (x1 - 10, y0 + int(h * 0.30))], fill=NAVY)
    col_top = y0 + int(h * 0.33)
    col_bot = y1 - int(h * 0.34)
    for i in range(3):
        col_x = x0 + 26 + i * ((x1 - x0 - 52) / 2)
        draw.rectangle([col_x - 6, col_top, col_x + 6, col_bot], fill=NAVY)
    draw.rectangle([x0 + 10, col_bot, x1 - 10, col_bot + 6], fill=NAVY)
    # scales of justice
    sy = y1 - int(h * 0.12)
    draw.line([(cx, sy - 13), (cx, sy)], fill=RED, width=3)
    draw.line([(cx - 20, sy - 13), (cx + 20, sy - 13)], fill=RED, width=3)
    for dx in (-20, 20):
        draw.line([(cx + dx, sy - 13), (cx + dx, sy - 5)], fill=RED, width=2)
        draw.arc([cx + dx - 9, sy - 7, cx + dx + 9, sy + 5], 0, 180,
                 fill=RED, width=2)


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    centred(d, W // 2, 16, "THE WORLD TODAY", font(SERIF_B, 86))
    rule(d, 118, MARGIN, W - MARGIN, 3)
    rule(d, 124, MARGIN, W - MARGIN, 1)
    centred(d, W // 2, 134, "Thursday, 19 November 2026",
            font(SERIF_B, 42), fill=RED)
    centred(d, W // 2, 186, "ONE DAY'S WORLD NEWS  •  SIX STORIES AND MORE",
            font(SANS, 19), fill=GREY)
    rule(d, 214, MARGIN, W - MARGIN, 3)
    rule(d, 219, MARGIN, W - MARGIN, 1)

    # ---- Lead story (full width) ----
    lx0, ly0, lx1, ly1 = MARGIN, 230, W - MARGIN, 404
    box(d, lx0, ly0, lx1, ly1)
    kicker(d, lx0 + 14, ly0 + 10, "LEAD STORY")
    headline(d, lx0 + 14, ly0 + 32, "TRUMP, XI AND PUTIN MEET IN "
             "FIRST-EVER SUMMIT", 32, 610)
    text_block(d, lx0 + 14, ly0 + 106,
               "The three leaders hold a three-way summit in Shenzhen, on "
               "the sidelines of APEC. Agenda: nuclear arms control, "
               "Ukraine and the war with Iran. No deal is expected.",
               font(SANS, 18), 600, leading=1.22)
    draw_flags_scene(d, lx1 - 330, ly0 + 12, lx1 - 12, ly1 - 12)

    # ---- Two-column story grid ----
    col_w = (W - 2 * MARGIN - 24) // 2
    rows = [
        (416, 580, [
            ("TECH  •  GAMES", "GTA 6 is out today",
             "GTA VI launches today on PlayStation 5 and Xbox Series X|S, "
             "with a rolling midnight-local unlock. File up to 212 GB; 99 "
             "on Metacritic.", draw_game_case),
            ("TECH  •  MARKETS", "Anthropic's $81.3bn IPO",
             "Anthropic's IPO prices at $83 a share, raising $81.3 "
             "billion — the largest on record. Shares trade on the Nasdaq "
             "today under ticker ANT.", draw_chart),
        ]),
        (592, 756, [
            ("EUROPE  •  CONFLICT", "Kerch Bridge hit again",
             "The Crimean Bridge is hit again overnight — the third attack "
             "this week. Traffic is suspended while damage is assessed.",
             draw_bridge),
            ("MIDDLE EAST  •  CONFLICT", "Tanker hit in Hormuz",
             "A tanker is hit in the Strait of Hormuz — engine-room "
             "strike, crew safe — as US–Iran strikes continue across the "
             "Gulf.", draw_tanker),
        ]),
    ]
    for y0, y1, cells in rows:
        for ci, (kick, head, body, art) in enumerate(cells):
            x0 = MARGIN + ci * (col_w + 24)
            x1 = x0 + col_w
            box(d, x0, y0, x1, y1)
            kicker(d, x0 + 12, y0 + 9, kick, size=16)
            headline(d, x0 + 12, y0 + 30, head, 27, col_w - 24)
            text_block(d, x0 + 12, y0 + 62, body, font(SANS, 17),
                       col_w - 160, leading=1.28)
            art(d, x1 - 136, y0 + 62, x1 - 12, y0 + 152)
            if kick.startswith("TECH  •  MARKETS"):
                d.text((x1 - 136, y0 + 9), "$83  •  ANT",
                       font=font(SANS_B, 18), fill=RED)

    # ---- Bottom row: The Hague + Also today ----
    by0, by1 = 768, 936
    bx0, bx1 = MARGIN, MARGIN + col_w
    box(d, bx0, by0, bx1, by1)
    kicker(d, bx0 + 12, by0 + 9, "THE HAGUE  •  LAW", size=16)
    headline(d, bx0 + 12, by0 + 30, "Rohingya ruling", 27, col_w - 24)
    text_block(d, bx0 + 12, by0 + 62,
               "The International Court of Justice delivers its judgment "
               "today on whether Myanmar committed genocide against the "
               "Rohingya. It would be a first for the court.",
               font(SANS, 17), col_w - 160, leading=1.15)
    draw_court(d, bx1 - 136, by0 + 62, bx1 - 12, by1 - 12)

    ax0, ax1 = MARGIN + col_w + 24, W - MARGIN
    box(d, ax0, by0, ax1, by1)
    kicker(d, ax0 + 12, by0 + 9, "ALSO TODAY", size=16)
    items = [
        ("ISRAEL:", "Herzog asks Gadi Eisenkot to form the next "
         "government, bypassing PM Netanyahu."),
        ("RELIGION:", "Pew report: Islam set to become the world's largest "
         "religion by 2035."),
        ("GAZA:", "Australia, Canada, Italy and the UK call on Israel to "
         "let aid reach flooded Gaza."),
    ]
    yy = by0 + 32
    for label, text in items:
        yy = text_block(d, ax0 + 12, yy, label + " " + text,
                        font(SANS, 17), ax1 - ax0 - 24, leading=1.2)
        yy += 5

    # Footer
    rule(d, 950, MARGIN, W - MARGIN, 2)
    centred(d, W // 2, 962, "All stories first reported 19 November 2026",
            font(SANS, 17), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
