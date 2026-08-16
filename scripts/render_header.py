"""Render assets/header.png for the GitHub profile README.

Edit the text, colors, or layout below, then run:

    .venv/bin/python scripts/render_header.py

That overwrites assets/header.png. The README points at the PNG, not the SVG.
"""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1500, 480
OUT = Path(__file__).resolve().parents[1] / "assets" / "header.png"

KICKER = "< blockchain  ·  backend />"
NAME = "Ali Murtaza Memon"
TAGLINE = "Building secure, scalable Web3 infrastructure"
SPECIALTIES = "Smart contracts  ·  Python & Node.js backends  ·  Protocol security"
CHIPS = [
    (92, 186, "Smart Energy Pay", (34, 211, 238)),
    (294, 200, "4+ Years Experience", (129, 140, 248)),
    (510, 214, "Chemnitz, Germany", (192, 132, 252)),
]


def lerp(a, b, t):
    return int(a + (b - a) * t)


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def load_mono(size):
    for path in (
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return load_font(size)


def paint_background(px):
    for y in range(H):
        for x in range(W):
            t = (x / (W - 1)) * 0.55 + (y / (H - 1)) * 0.45
            r = lerp(7, 16, t)
            g = lerp(11, 24, t)
            b = lerp(20, 42, t)
            dx, dy = (x - 270) / 520, (y - 190) / 280
            cyan = max(0.0, 1.0 - (dx * dx + dy * dy))
            dx2, dy2 = (x - 1290) / 480, (y - 280) / 300
            purp = max(0.0, 1.0 - (dx2 * dx2 + dy2 * dy2))
            r = min(255, int(r + 34 * cyan * 0.35 + 167 * purp * 0.28))
            g = min(255, int(g + 211 * cyan * 0.22 + 139 * purp * 0.12))
            b = min(255, int(b + 238 * cyan * 0.28 + 250 * purp * 0.26))
            px[x, y] = (r, g, b)


def hexagon(draw, cx, cy, radius, outline, fill=None):
    pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        pts.append((cx + radius * math.cos(angle),
                   cy + radius * math.sin(angle)))
    draw.polygon(pts, fill=fill, outline=outline)


def main():
    img = Image.new("RGB", (W, H), "#070B14")
    paint_background(img.load())
    draw = ImageDraw.Draw(img, "RGBA")

    for x in range(0, W, 48):
        draw.line([(x, 0), (x, H)], fill=(147, 197, 253, 16), width=1)
    for y in range(0, H, 48):
        draw.line([(0, y), (W, y)], fill=(147, 197, 253, 16), width=1)

    for y in range(H):
        t = y / (H - 1)
        if t < 0.5:
            u = t * 2
            color = (lerp(34, 129, u), lerp(211, 140, u), lerp(238, 248, u))
        else:
            u = (t - 0.5) * 2
            color = (lerp(129, 192, u), lerp(140, 132, u), lerp(248, 252, u))
        draw.line([(0, y), (7, y)], fill=color)

    hexagon(draw, 1280, 126, 46, (103, 232, 249, 50), (34, 211, 238, 22))
    hexagon(draw, 1368, 210, 38, (103, 232, 249, 46), (167, 139, 250, 22))
    hexagon(draw, 1228, 290, 38, (103, 232, 249, 40))
    hexagon(draw, 1410, 332, 30, (103, 232, 249, 40))

    draw.text((92, 92), KICKER, font=load_mono(18), fill=(103, 232, 249))
    draw.text((92, 142), NAME, font=load_font(
        58, bold=True), fill=(248, 250, 252))

    for x in range(92, 372):
        t = (x - 92) / 280
        if t < 0.5:
            u = t * 2
            color = (lerp(34, 129, u), lerp(211, 140, u), lerp(238, 248, u))
        else:
            u = (t - 0.5) * 2
            color = (lerp(129, 192, u), lerp(140, 132, u), lerp(248, 252, u))
        draw.line([(x, 226), (x, 229)], fill=color)

    draw.text((92, 252), TAGLINE, font=load_font(24), fill=(203, 213, 225))
    draw.text((92, 294), SPECIALTIES, font=load_font(20), fill=(148, 163, 184))

    chip_font = load_font(16)
    for x, width, label, stroke in CHIPS:
        draw.rounded_rectangle(
            [x, 360, x + width, 404],
            radius=20,
            fill=(15, 23, 42),
            outline=stroke,
            width=2,
        )
        bbox = draw.textbbox((0, 0), label, font=chip_font)
        text_width = bbox[2] - bbox[0]
        draw.text((x + (width - text_width) / 2, 372), label,
                  font=chip_font, fill=(226, 232, 240))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
