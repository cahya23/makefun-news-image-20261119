"""Render the front page for the news-image-20261119 entry.

Draws "THE WORLD TODAY", a newspaper front page summing up Thursday
19 November 2026, programmatically with PIL. No network, no downloaded
images: every picture on the page is drawn in code from shapes.

Run:  python3 render.py
Writes entry.png next to this file (1024x1024, deterministic).
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 240, 221)
INK = (17, 17, 17)
RED = (163, 30, 34)
RULE = (17, 17, 17)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split():
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


def text_block(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def story_box(draw, x, y, w, h, kicker, headline, body, art):
    """One bordered story box with a small drawn illustration at right."""
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    pad = 14
    tx = x + pad
    ty = y + 10
    draw.text((tx, ty), kicker, font=font(SANS_B, 14), fill=RED)
    ty += 24
    art_w = 116
    text_w = w - pad * 2 - art_w - 12
    ty = text_block(draw, tx, ty, headline, font(SERIF_B, 23),
                    text_w, 27)
    ty += 4
    text_block(draw, tx, ty, body, font(SANS, 17), text_w, 21)
    art(draw, x + w - pad - art_w, y + 38, art_w, 110)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    draw.ellipse([x + 5, y + 5, x + 13, y + 13], fill=(255, 222, 0))
    for dx, dy in ((20, 4), (24, 10), (24, 17), (20, 22)):
        draw.ellipse([x + dx, y + dy, x + dx + 4, y + dy + 4],
                     fill=(255, 222, 0))


def flag_usa(draw, x, y, w, h):
    for i in range(7):
        col = (179, 25, 66) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                       fill=col)
    draw.rectangle([x, y, x + w * 2 // 5, y + h * 4 // 7],
                   fill=(10, 49, 97))


def flag_russia(draw, x, y, w, h):
    for i, col in enumerate(((255, 255, 255), (0, 57, 166),
                             (213, 0, 50))):
        draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3],
                       fill=col)


def art_lead(draw, x, y, w, h):
    """Shenzhen skyline with the flags of China, the US and Russia."""
    draw.rectangle([x, y, x + w, y + h], fill=(207, 227, 242))
    # Skyline.
    base = y + h - 26
    skyline = [(0, 46), (34, 70), (70, 38), (104, 62), (140, 30),
               (176, 58), (210, 44), (244, 66), (278, 40)]
    for bx, bh in skyline:
        draw.rectangle([x + bx, base - bh, x + bx + 30, base],
                       fill=(85, 85, 85))
    # Three flag poles.
    for i, fn in enumerate((flag_china, flag_usa, flag_russia)):
        px = x + 30 + i * 108
        draw.rectangle([px, y + 16, px + 4, base], fill=(60, 60, 60))
        fn(draw, px + 4, y + 16, 56, 36)
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(44, 74, 107))
    draw.text((x + 10, y + h - 22), "SHENZHEN  •  APEC",
              font=font(SANS_B, 13), fill=(255, 255, 255))


def fit_font(path, text, start, max_w):
    """Largest size at or below start whose text fits max_w."""
    size = start
    while size > 12:
        fnt = font(path, size)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(
                text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, 12)


def art_gta(draw, x, y, w, h):
    """Night city skyline with a big VI for the GTA 6 launch."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    # Stars.
    for sx, sy in ((10, 10), (30, 22), (52, 8), (76, 18), (98, 8)):
        draw.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                     fill=(255, 255, 255))
    # Skyline silhouette.
    base = y + h - 24
    for bx, bh in ((0, 34), (26, 52), (54, 28), (80, 44)):
        draw.rectangle([x + bx, base - bh, x + bx + 24, base],
                       fill=(60, 70, 110))
    # Big VI.
    draw.text((x + 28, y + 30), "VI", font=font(SERIF_B, 44),
              fill=(255, 255, 255))
    draw.rectangle([x, y + h - 24, x + w, y + h], fill=(179, 25, 66))
    draw.text((x + 6, y + h - 20), "OUT TODAY",
              font=font(SANS_B, 11), fill=(255, 255, 255))


def art_anthropic(draw, x, y, w, h):
    """Rising chart and $83 for the Anthropic IPO."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 245, 238))
    # Rising chart arrow.
    draw.line([x + 8, y + 74, x + 34, y + 58, x + 52, y + 64, x + 78,
               y + 40], fill=(26, 122, 46), width=3)
    draw.polygon([(x + 78, y + 40), (x + 66, y + 40), (x + 78, y + 52)],
                 fill=(26, 122, 46))
    draw.text((x + 30, y + 14), "$83", font=font(SERIF_B, 30),
              fill=(163, 30, 34))
    draw.text((x + 6, y + h - 14), "NASDAQ: ANT",
              font=font(SANS_B, 10), fill=(60, 60, 60))


def art_kerch(draw, x, y, w, h):
    """Broken bridge over the Kerch Strait."""
    draw.rectangle([x, y, x + w, y + h], fill=(223, 234, 242))
    # Water.
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(61, 122, 181))
    for wx in range(x + 4, x + w - 8, 18):
        draw.arc([wx, y + h - 26, wx + 14, y + h - 14], 180, 360,
                 fill=(255, 255, 255), width=2)
    # Deck in two pieces with a gap in the middle, over the water.
    draw.rectangle([x + 2, y + 30, x + 46, y + 40], fill=(60, 60, 60))
    draw.rectangle([x + 70, y + 30, x + 114, y + 40], fill=(60, 60, 60))
    # Fallen span, tilted down through the gap into the water.
    draw.polygon([(x + 50, y + 42), (x + 62, y + 40),
                  (x + 70, y + 68), (x + 58, y + 70)], fill=(90, 90, 90))
    # Fallen piece in the water.
    draw.polygon([(x + 58, y + h - 34), (x + 84, y + h - 26),
                  (x + 80, y + h - 18), (x + 56, y + h - 24)],
                 fill=(90, 90, 90))
    draw.text((x + 6, y + h - 16), "KERCH STRAIT",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def art_gulf(draw, x, y, w, h):
    """Tanker on the Strait of Hormuz with a blast burst."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 210))
    # Sea.
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(61, 122, 181))
    for wx in range(x + 4, x + w - 8, 18):
        draw.arc([wx, y + h - 30, wx + 14, y + h - 18], 180, 360,
                 fill=(255, 255, 255), width=2)
    # Tanker hull and bridge.
    draw.rectangle([x + 10, y + 62, x + 96, y + 78], fill=(90, 40, 40))
    draw.rectangle([x + 70, y + 44, x + 92, y + 62], fill=(220, 220, 220),
                   outline=(60, 60, 60))
    draw.rectangle([x + 18, y + 50, x + 60, y + 62], fill=(180, 60, 60))
    # Blast burst above the tanker.
    cx, cy = x + 40, y + 28
    pts = []
    for i in range(12):
        r = 18 if i % 2 == 0 else 8
        ang = math.pi * i / 6
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=(30, 30, 30))
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(120, 120, 120))
    draw.text((x + 6, y + h - 16), "STRAIT OF HORMUZ",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def art_icj(draw, x, y, w, h):
    """Courthouse in The Hague with columns and scales."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 238, 240))
    # Pediment.
    draw.polygon([(x + 14, y + 34), (x + 58, y + 10), (x + 102, y + 34)],
                 fill=(120, 120, 130))
    # Columns.
    for cx in (24, 44, 64, 84):
        draw.rectangle([x + cx, y + 36, x + cx + 8, y + 78],
                       fill=(200, 200, 210), outline=(90, 90, 90))
    draw.rectangle([x + 14, y + 78, x + 102, y + 86], fill=(90, 90, 90))
    draw.text((x + 6, y + h - 14), "THE HAGUE",
              font=font(SANS_B, 10), fill=(60, 60, 60))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.text((W // 2, 20), "THE WORLD TODAY", font=font(SERIF_B, 62),
           fill=INK, anchor="ma")
    d.line([28, 96, W - 28, 96], fill=RULE, width=3)
    d.text((W // 2, 106), "Thursday, 19 November 2026",
           font=font(SERIF_B, 36), fill=RED, anchor="ma")
    d.text((W // 2, 152), "ONE DAY'S WORLD NEWS  •  SIX STORIES AND MORE",
           font=font(SANS, 15), fill=(80, 80, 80), anchor="ma")
    d.line([28, 178, W - 28, 178], fill=RULE, width=2)

    # Lead story.
    lx, ly, lw, lh = 28, 190, 968, 190
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=RULE, width=2)
    d.text((lx + 16, ly + 10), "LEAD STORY", font=font(SANS_B, 15),
           fill=RED)
    d.text((lx + 16, ly + 32), "TRUMP, XI AND PUTIN MEET",
           font=fit_font(SERIF_B, "TRUMP, XI AND PUTIN MEET", 36, 620),
           fill=INK)
    d.text((lx + 16, ly + 68), "FIRST-EVER SUMMIT IN SHENZHEN",
           font=fit_font(SERIF_B, "FIRST-EVER SUMMIT IN SHENZHEN", 36,
                         620), fill=INK)
    text_block(d, lx + 16, ly + 116,
               "Donald Trump, Xi Jinping and Vladimir Putin hold the "
               "first-ever three-way summit at Kylin Villa, on the "
               "APEC sidelines. Agenda: nuclear arms, Ukraine and the "
               "war with Iran.",
               font(SANS, 19), 596, 24)
    art_lead(d, lx + 640, ly + 14, 312, 162)

    # Grid: four stories.
    gx = [28, 520]
    gy = [392, 568]
    gw, gh = 476, 164
    stories = [
        ("TECH • GAMES", "GTA 6 is out today",
         "GTA VI launches on PS5 and Xbox Series X|S. File up to "
         "212 GB; 99 on Metacritic; no PC version.",
         art_gta),
        ("BUSINESS • IPO", "Anthropic's record $81.3bn IPO",
         "Anthropic's IPO prices at $83 a share, raising $81.3bn — "
         "the largest ever. Shares trade today as ANT.",
         art_anthropic),
        ("EUROPE • CONFLICT", "Kerch Bridge hit a third time",
         "The Crimean Bridge is hit a third time this week. "
         "Traffic is suspended while damage is assessed.",
         art_kerch),
        ("MIDDLE EAST • CONFLICT", "Tanker struck in the Strait of Hormuz",
         "A tanker is hit in the Strait of Hormuz as US–Iran "
         "strikes continue; Trump warns of Iranian chemical arms.",
         art_gulf),
    ]
    for i, (kicker, head, body, art) in enumerate(stories):
        story_box(d, gx[i % 2], gy[i // 2], gw, gh, kicker, head, body,
                  art)

    # Bottom row: ICJ + also today.
    story_box(d, 28, 744, 476, 164, "WORLD • JUSTICE",
              "The Hague rules on Rohingya genocide",
              "The ICJ rules today on Myanmar and the Rohingya "
              "genocide — the first time a state faces such a verdict.",
              art_icj)

    ax, ay, aw, ah = 520, 744, 476, 164
    d.rectangle([ax, ay, ax + aw, ay + ah], outline=RULE, width=2)
    d.text((ax + 14, ay + 10), "ALSO TODAY", font=font(SANS_B, 14),
           fill=RED)
    items = [
        ("ISRAEL: ", "Herzog asks ex-army chief Eisenkot to form the "
         "next government, bypassing Netanyahu."),
        ("FAITH: ", "Pew report: Islam set to become the world's "
         "largest religion by 2035."),
        ("GAZA: ", "Australia, Canada, Italy and the UK call on "
         "Israel to let aid reach flooded Gaza."),
    ]
    iy = ay + 36
    for lead, rest in items:
        f_lead = font(SANS_B, 16)
        f_rest = font(SANS, 16)
        full = lead + rest
        lines = wrap(d, full, f_rest, aw - 28)
        for j, line in enumerate(lines):
            if j == 0:
                d.text((ax + 14, iy), lead, font=f_lead, fill=INK)
                lw = d.textlength(lead, font=f_lead)
                d.text((ax + 14 + lw, iy), line[len(lead):],
                       font=f_rest, fill=INK)
            else:
                d.text((ax + 14, iy), line, font=f_rest, fill=INK)
            iy += 20
        iy += 4

    # Footer.
    d.line([28, 922, W - 28, 922], fill=RULE, width=2)
    d.text((W // 2, 936), "All stories first reported 19 November 2026",
           font=font(SANS, 15), fill=(80, 80, 80), anchor="ma")

    img.save("entry.png")


if __name__ == "__main__":
    main()
