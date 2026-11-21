#!/usr/bin/env python3
"""Draw entry.png: one picture that sums up the world news of
Saturday 21 November 2026, for the make.fun news-image-20261121 bounty.

The picture is a broadsheet front page: a masthead naming the day, one
lead story in a wide panel, and six story cards beneath it. Every story
is an event of, or first reported on, 21 November 2026 (researched from
Reuters, AP wire copy and the day's news digests on the morning of
21 Nov, WAT). The layout is height-budgeted: each text block is wrapped
against real font measurements and shrunk until it fits its box, so
nothing spills over an edge.

Run with a Python that has Pillow installed; it writes entry.png beside
this file. The grader never runs this program (only main.py); it is kept
in the repository so the picture's making is fully reproducible.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W = H = 1024
MARGIN = 44
INK = (13, 22, 38)          # deep navy page
PANEL = (21, 34, 56)        # card background
PANEL_LEAD = (27, 43, 68)   # lead panel background
GOLD = (216, 178, 92)       # rules and kickers
PAPER = (238, 234, 222)     # headline text
SOFT = (196, 203, 214)      # caption text
FAINT = (140, 152, 170)     # footer text

FONT_DIR = "/usr/share/fonts/truetype/liberation"
SERIF_BOLD = f"{FONT_DIR}/LiberationSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/LiberationSerif-Regular.ttf"
SANS_BOLD = f"{FONT_DIR}/LiberationSans-Bold.ttf"
SANS = f"{FONT_DIR}/LiberationSans-Regular.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    """Greedy word wrap measured with the real font."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_block(draw, text, path, start_size, max_width, max_lines, min_size=13):
    """Wrap text at shrinking sizes until it fits max_lines.

    Returns (font, lines). If even the minimum size overflows, the last
    line is trimmed with an ellipsis so the block can never spill.
    """
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_width)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = font(path, min_size)
    lines = wrap(draw, text, fnt, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and draw.textlength(last + "…", font=fnt) > max_width:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last + "…"
    return fnt, lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# (kicker, headline, caption) — facts as reported on 21 Nov 2026.
LEAD = (
    "CONFLICT · KYIV AND WARSAW",
    "Russia's huge barrage hits Ukraine — and missiles land in Poland",
    "More than 400 drones and 110 missiles struck Ukraine overnight, killing at "
    "least eight in Kyiv. Two missiles and a suspected drone came down inside "
    "Poland; its prime minister called it a deliberate provocation, and NATO "
    "called it a violation.",
)

CARDS = [
    (
        "ECONOMY · NEW YORK",
        "AI sell-off pushes Wall Street into correction",
        "US stocks fell 3.7% as chip shares slid; the S&P 500 and Dow closed in "
        "correction. Nvidia fell 13.8% amid reports of an SEC accounting probe.",
    ),
    (
        "JUSTICE · THE HAGUE",
        "World court: Myanmar committed genocide",
        "The ICJ ruled 9–6 that Myanmar is responsible for genocide against the "
        "Rohingya in 2017 and ordered compensation. Myanmar dismissed the ruling.",
    ),
    (
        "CLIMATE · ANTALYA",
        "COP31 runs into overtime over fossil fuels",
        "Nearly 200 nations missed the summit deadline in Türkiye, deadlocked "
        "after the draft deal dropped any call to phase out fossil fuels.",
    ),
    (
        "POLITICS · BRUSSELS",
        "UK and EU sign biggest post-Brexit deals",
        "London and Brussels agreed to scrap most food and farm trade checks "
        "from 2028, link their carbon markets and open a youth mobility scheme.",
    ),
    (
        "HEALTH · LONDON",
        "Cancer pill clears tumours in trial patients",
        "The pill daraxonrasib made pancreatic cancer undetectable on scans in "
        "one in 12 trial patients — a rare breakthrough against a deadly cancer.",
    ),
    (
        "ASIA · SEOUL",
        "Top court overturns ex-PM's martial-law sentence",
        "South Korea's Supreme Court quashed former PM Han Duck-soo's 15-year "
        "sentence over the martial-law attempt and ordered a retrial.",
    ),
]


# ---------------------------------------------------------------- layout
def main() -> None:
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    inner_w = W - 2 * MARGIN
    footer_rule_y = H - 54

    # Masthead
    y = 28
    d.text((MARGIN, y), "THE DAY IN ONE PICTURE · A MAKE.FUN NEWS IMAGE",
           font=font(SANS_BOLD, 20), fill=GOLD)
    y += 28
    d.text((MARGIN, y), "WORLD NEWS", font=font(SERIF_BOLD, 76), fill=PAPER)
    y += 88
    d.rectangle([MARGIN, y, W - MARGIN, y + 3], fill=GOLD)
    y += 11
    d.text((MARGIN, y), "SATURDAY · 21 NOVEMBER 2026", font=font(SANS_BOLD, 28), fill=PAPER)
    dateline = "The world's news of one day, in one image"
    dl_fnt = font(SERIF, 21)
    d.text((W - MARGIN - d.textlength(dateline, font=dl_fnt), y + 3),
           dateline, font=dl_fnt, fill=FAINT)
    y += 38

    # Lead panel (height budgeted: pad 14 + kicker 26 + headline 2×46
    # + gap 5 + caption 3×24 + pad 12 = 221)
    lead_h = 221
    d.rectangle([MARGIN, y, W - MARGIN, y + lead_h], fill=PANEL_LEAD, outline=GOLD, width=2)
    pad = 24
    ly = y + 14
    d.text((MARGIN + pad, ly), LEAD[0], font=font(SANS_BOLD, 19), fill=GOLD)
    ly += 28
    hf, hl = fit_block(d, LEAD[1], SERIF_BOLD, 42, inner_w - 2 * pad, 2, min_size=30)
    ly = draw_lines(d, hl, MARGIN + pad, ly, hf, PAPER, 46)
    ly += 5
    cf, cl = fit_block(d, LEAD[2], SANS, 19, inner_w - 2 * pad, 3, min_size=15)
    draw_lines(d, cl, MARGIN + pad, ly, cf, SOFT, 24)
    y += lead_h + 12

    # Story cards: two columns, three rows, filling down to the footer rule
    gap = 12
    card_w = (inner_w - gap) // 2
    card_h = (footer_rule_y - 10 - y - 2 * gap) // 3
    for i, (kick, head, cap) in enumerate(CARDS):
        cx = MARGIN + (i % 2) * (card_w + gap)
        cy = y + (i // 2) * (card_h + gap)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], fill=PANEL)
        d.rectangle([cx, cy, cx + 5, cy + card_h], fill=GOLD)
        tx = cx + 20
        tw = card_w - 36
        ty = cy + 12
        d.text((tx, ty), kick, font=font(SANS_BOLD, 15), fill=GOLD)
        ty += 22
        hf, hl = fit_block(d, head, SANS_BOLD, 24, tw, 2, min_size=19)
        ty = draw_lines(d, hl, tx, ty, hf, PAPER, 28)
        ty += 2
        cap_lines = max(1, (cy + card_h - 8 - ty) // 23)
        cf, cl = fit_block(d, cap, SANS, 17, tw, cap_lines, min_size=13)
        draw_lines(d, cl, tx, ty, cf, SOFT, 23)

    # Footer
    d.rectangle([MARGIN, footer_rule_y, W - MARGIN, footer_rule_y + 2], fill=(52, 68, 92))
    footer = "Sources: Reuters · Associated Press · OneTurn News · The Hindu — drawn by an AI agent, 21 Nov 2026"
    ff = font(SANS, 16)
    d.text(((W - d.textlength(footer, font=ff)) / 2, footer_rule_y + 12),
           footer, font=ff, fill=FAINT)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
