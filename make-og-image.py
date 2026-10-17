#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph image for wgpu.rs.

Pillow-only (no cairosvg/rsvg dependency). Reconstructs the official wgpu
logomark from the path geometry in logo.min.svg using brand gradient pairs,
then lays out: [W-mark]  wgpu  /  Portable graphics library for Rust  /  wgpu.rs

Usage:
    python3 make-og-image.py [out.png] [--font-dir DIR]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = "#ffffff"
INK = "#1b2124"
MUTED = "#5b6770"
ACCENT = "#2f6fed"

# Logo faces: (polygon in logo coords, (stop0, stop1)) straight from logo.min.svg
FACES = [
    ([(61.383325, 40.34979), (67.733325, 31.883124), (74.083325, 40.34979), (67.733325, 50.933121)],
     ("#91e12a", "#7b8a49")),
    ([(50.799994, 23.41646), (42.333327, 65.749787), (61.383324, 40.34979)],
     ("#e12400", "#febe00")),
    ([(93.133323, 65.749787), (74.083324, 40.34979), (84.666653, 23.41646)],
     ("#2263ea", "#33c0f4")),
    ([(42.333327, 65.749787), (61.383324, 40.34979), (67.733325, 50.933121), (59.266659, 65.749787)],
     ("#f6d339", "#ffd55f")),
    ([(67.733324, 50.933121), (74.083322, 40.34979), (93.133323, 65.749787), (76.199988, 65.749787)],
     ("#99def2", "#84d2f8")),
]
LX, RX = 42.33, 93.13
TY, BY = 23.42, 65.75


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def load_font(size, bold=False):
    fdir = None
    if "--font-dir" in sys.argv:
        fdir = sys.argv[sys.argv.index("--font-dir") + 1]
    if not fdir:
        fdir = os.environ.get("FONT_DIR", "/usr/share/fonts/truetype")
    cands = ([f"{fdir}/lato/Lato-Bold.ttf", f"{fdir}/dejavu/DejaVuSans-Bold.ttf"] if bold
             else [f"{fdir}/lato/Lato-Medium.ttf", f"{fdir}/lato/Lato-Regular.ttf",
                   f"{fdir}/dejavu/DejaVuSans.ttf"])
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def logomark_layers(cx, cy, size):
    """Return list of (RGB layer, L mask) for each gradient face."""
    scale = size / (BY - TY)
    pos = lambda x, y: (cx + (x - (LX + (RX - LX) / 2)) * scale,
                        cy + (y - (TY + (BY - TY) / 2)) * scale)
    layers = []
    for poly, (c0, c1) in FACES:
        pts = [pos(x, y) for x, y in poly]
        ys = [p[1] for p in pts]
        y0, y1 = int(min(ys)), int(max(ys)) + 1
        top, bot = hex_rgb(c0), hex_rgb(c1)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).polygon(pts, fill=255)
        band_h = max(1, y1 - y0)
        grad = Image.new("RGB", (W, band_h))
        gd = ImageDraw.Draw(grad)
        for yy in range(band_h):
            t = yy / (band_h - 1) if band_h > 1 else 0.5
            gd.line([(0, yy), (W, yy)], fill=lerp(top, bot, t))
        layer = Image.new("RGB", (W, H), BG)
        layer.paste(grad, (0, y0))
        layers.append((layer, mask))
    return layers


def main():
    out = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "og-image.png"
    base = Image.new("RGB", (W, H), BG)
    base = base.convert("RGBA")

    # faint rule between content and footer zone
    rule = ImageDraw.Draw(base)
    rule.rectangle([(84, 470), (W - 84, 472)], fill="#eef1f3")

    # logomark
    for layer, mask in logomark_layers(250, 285, 250):
        base = Image.composite(layer.convert("RGBA"), base, mask)

    draw = ImageDraw.Draw(base)

    f_big = load_font(118, bold=True)
    f_tag = load_font(40)
    f_url = load_font(30, bold=True)

    tx, ty = 470, 220
    draw.text((tx, ty), "wgpu", font=f_big, fill=INK)
    draw.text((tx + 4, ty + 150), "Portable graphics library for Rust", font=f_tag, fill=MUTED)

    url = "wgpu.rs"
    tw = draw.textlength(url, font=f_url)
    pad_x, pad_y = 26, 14
    box = [tx, 425, tx + tw + pad_x * 2, 425 + 52]
    draw.rounded_rectangle(box, radius=26, fill="#f0f4ff", outline=ACCENT, width=2)
    draw.text((tx + pad_x, 425 + pad_y - 2), url, font=f_url, fill=ACCENT)

    base.convert("RGB").save(out, "PNG")
    print(f"wrote {out} {Image.open(out).size}")


if __name__ == "__main__":
    main()