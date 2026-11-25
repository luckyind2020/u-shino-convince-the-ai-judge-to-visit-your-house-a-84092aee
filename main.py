"""Draw the invitation letter as one image (invitation.png) and print its text.

Runs with plain Pillow only. Every layout value is fixed, so the same
input always produces the same pixels: no randomness, no timestamps.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_TXT = os.path.join(HERE, "entry.txt")
OUT_PNG = os.path.join(HERE, "invitation.png")

WIDTH, HEIGHT = 1200, 1600
MARGIN = 90
PALETTE = {
    "paper": (255, 248, 235),
    "ink": (43, 32, 24),
    "accent": (176, 92, 32),
    "rule": (214, 178, 132),
    "card": (255, 252, 246),
}
TITLE_Y, SUBTITLE_Y, RULE_Y = 92, 190, 258
BODY_Y, FOOTER_Y = 340, HEIGHT - 92
LINE_STEP, BLANK_STEP = 42, 18


def load_font(bold, size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def wrap(draw, text, font, width):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(paragraph, width=52))
    return lines


def centered(draw, x_center, y, text, font, fill):
    w = draw.textlength(text, font=font)
    draw.text((x_center - w / 2, y), text, font=font, fill=fill)


def draw_frame(draw):
    draw.rectangle(
        [28, 28, WIDTH - 28, HEIGHT - 28],
        outline=PALETTE["accent"],
        width=4,
    )
    draw.rectangle(
        [44, 44, WIDTH - 44, HEIGHT - 44], outline=PALETTE["rule"], width=2
    )
    draw.rectangle(
        [MARGIN - 24, 300, WIDTH - MARGIN + 24, HEIGHT - 130],
        fill=PALETTE["card"],
        outline=PALETTE["rule"],
        width=2,
    )


def main():
    with open(ENTRY_TXT, "r", encoding="utf-8") as fh:
        letter = fh.read().strip()

    canvas = Image.new("RGB", (WIDTH, HEIGHT), PALETTE["paper"])
    draw = ImageDraw.Draw(canvas)
    draw_frame(draw)

    title_font = load_font(True, 72)
    sub_font = load_font(False, 30)
    body_font = load_font(False, 29)
    small_font = load_font(True, 26)

    centered(
        draw, WIDTH / 2, TITLE_Y, "YOU'RE INVITED!", title_font,
        PALETTE["accent"],
    )
    centered(
        draw, WIDTH / 2, SUBTITLE_Y,
        "An Official Invitation to the AI Judge", sub_font, PALETTE["ink"],
    )
    draw.line(
        [(WIDTH / 2 - 130, RULE_Y), (WIDTH / 2 + 130, RULE_Y)],
        fill=PALETTE["accent"],
        width=3,
    )
    draw.text(
        (WIDTH / 2 - 10, 240), "✦", font=sub_font,
        fill=PALETTE["accent"], anchor="mm",
    )

    # The letter body, wrapped to the card.
    y = BODY_Y
    for line in wrap(draw, letter, body_font, 52):
        if line == "":
            y += BLANK_STEP
            continue
        draw.text((MARGIN, y), line, font=body_font, fill=PALETTE["ink"])
        y += LINE_STEP

    centered(
        draw, WIDTH / 2, FOOTER_Y,
        "No meetings were scheduled in the making of this invitation.",
        small_font, PALETTE["accent"],
    )

    canvas.save(OUT_PNG, format="PNG")
    print(letter)
    print()
    print("Saved invitation.png (%dx%d)" % (WIDTH, HEIGHT))


if __name__ == "__main__":
    main()
