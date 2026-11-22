#!/usr/bin/env python3
"""Generate the Lila animated eye emoji collection.

Lila is a girl: two big eyes with long, curved eyelashes, drawn with a tiny
palette so every 240x240 GIF stays small enough for the 4 MB assets
partition.  The output is consumed by ``scripts/build_default_assets.py``
through the local ``lila-gif`` emoji collection.

Usage::

    python main/assets/emoji/lila-gif/generate_eyes.py [--out DIR]

Requires Pillow (``python -m pip install pillow``).  The script is a design
tool, not part of the firmware build.
"""

import argparse
import math
import os

from PIL import Image, ImageDraw

W = H = 240
FRAME_MS = 100

# Palette indices.  Keep this list short: each extra colour costs bytes in
# every frame of every animation.
BLACK = 0
WHITE = 1
LILAC = 2
VIOLET = 3
DEEP = 4
PINK = 5
TEAR = 6

PALETTE = [
    (0, 0, 0),
    (255, 255, 255),
    (201, 167, 255),
    (124, 77, 255),
    (43, 16, 85),
    (255, 92, 158),
    (154, 220, 255),
]
FLAT_PALETTE = [c for rgb in PALETTE for c in rgb]

EYE_CX = (72, 168)
EYE_CY = 118
EYE_RX = 42
EYE_RY = 50


def new_scene():
    img = Image.new("P", (W, H), BLACK)
    img.putpalette(FLAT_PALETTE)
    return img, ImageDraw.Draw(img)


def _layer():
    layer = Image.new("P", (W, H), BLACK)
    layer.putpalette(FLAT_PALETTE)
    return layer, ImageDraw.Draw(layer)


def blush(d, cx, cy):
    """Three diagonal strokes on the cheek, the anime shorthand for a blush."""
    for i in range(3):
        x = cx - 7 + i * 8
        d.line([(x, cy), (x + 7, cy + 11)], fill=PINK, width=3)


def star(d, cx, cy, r, color):
    k = r * 0.28
    d.polygon(
        [
            (cx, cy - r),
            (cx + k, cy - k),
            (cx + r, cy),
            (cx + k, cy + k),
            (cx, cy + r),
            (cx - k, cy + k),
            (cx - r, cy),
            (cx - k, cy - k),
        ],
        fill=color,
    )


def heart(d, cx, cy, r, color):
    d.ellipse((cx - r, cy - r * 0.95, cx, cy + r * 0.15), fill=color)
    d.ellipse((cx, cy - r * 0.95, cx + r, cy + r * 0.15), fill=color)
    d.polygon([(cx - r * 0.95, cy - r * 0.15), (cx + r * 0.95, cy - r * 0.15), (cx, cy + r)], fill=color)


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def tapered(d, p0, p1, w0, w1, color, steps=4, bend=0.0):
    """Draw a stroke that thins out, optionally bent sideways."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / length, dx / length
    prev = p0
    for s in range(1, steps + 1):
        t = s / steps
        cur = _lerp(p0, p1, t)
        cur = (cur[0] + nx * bend * math.sin(math.pi * t), cur[1] + ny * bend * math.sin(math.pi * t))
        width = max(1, round(w0 + (w1 - w0) * t))
        d.line([prev, cur], fill=color, width=width)
        prev = cur


def bezier(p0, p1, p2, steps=12):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def stroke(d, pts, w0, w1, color, steps=None):
    n = steps or len(pts) - 1
    for i in range(min(n, len(pts) - 1)):
        t = i / max(1, n - 1)
        d.line([pts[i], pts[i + 1]], fill=color, width=max(1, round(w0 + (w1 - w0) * t)))


def lashes(d, cx, cy, rx, ry, open_ratio, out, scale=1.0, color=DEEP):
    """A fan of long, curved lashes on the outer top corner of one eye."""
    top = cy - ry * open_ratio
    cy_mid = (top + cy + ry) / 2
    ry_mid = (cy + ry - top) / 2
    for base_angle, length, width in ((198, 20.0, 6), (214, 27.0, 7), (231, 30.0, 7), (247, 25.0, 6)):
        angle = math.radians(base_angle if out < 0 else 540 - base_angle)
        bx = cx + rx * 1.01 * math.cos(angle)
        by = cy_mid + ry_mid * 1.01 * math.sin(angle)
        ln = length * scale
        tip = (bx + out * ln * 0.72, by - ln * 0.98)
        ctrl = (bx + out * ln * 0.62, by - ln * 0.18)
        stroke(d, bezier((bx, by), ctrl, tip), width, 1, color)


def liner(d, cx, cy, rx, ry, open_ratio, out):
    """Thick upper-lid line that ends in a small wing at the outer corner."""
    top = cy - ry * open_ratio
    cy_mid = (top + cy + ry) / 2
    ry_mid = (cy + ry - top) / 2
    pts = []
    for i in range(13):
        angle = math.radians(196 + (344 - 196) * i / 12)
        if out > 0:
            angle = math.radians(540 - math.degrees(angle))
        pts.append((cx + rx * math.cos(angle), cy_mid + ry_mid * math.sin(angle)))
    stroke(d, pts, 9, 4, DEEP)
    # Wing: extend the outer endpoint outwards and slightly up.
    outer = pts[0]
    tip = (outer[0] + out * 15, outer[1] - 1)
    ctrl = (outer[0] + out * 8, outer[1] - 4)
    stroke(d, bezier(outer, ctrl, tip), 7, 1, DEEP)


def open_eye(img, d, cx, cy, open_ratio=1.0, lookx=0, looky=0, pupil="round",
             lash_scale=1.0, lashes_on=True):
    rx, ry = EYE_RX, EYE_RY
    open_ratio = max(0.14, min(1.0, open_ratio))
    top = cy - ry * open_ratio
    bbox = (cx - rx, top, cx + rx, cy + ry)
    out = -1 if cx < W / 2 else 1

    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse(bbox, fill=255)
    layer, ld = _layer()
    ld.ellipse(bbox, fill=WHITE)

    icx, icy = cx + lookx, cy + looky
    r = 25
    if pupil == "heart":
        ld.ellipse((icx - r, icy - r, icx + r, icy + r), fill=VIOLET)
        ld.ellipse((icx - r, icy - r, icx + r, icy + r), outline=LILAC, width=3)
        heart(ld, icx, icy, 14, PINK)
    elif pupil == "star":
        star(ld, icx, icy, 20, LILAC)
        ld.ellipse((icx - 4, icy - 4, icx + 4, icy + 4), fill=WHITE)
    elif pupil == "small":
        ld.ellipse((icx - r, icy - r, icx + r, icy + r), fill=VIOLET)
        ld.ellipse((icx - 8, icy - 8, icx + 8, icy + 8), fill=DEEP)
        ld.ellipse((icx - 4, icy - 6, icx + 1, icy - 1), fill=WHITE)
    else:
        ld.ellipse((icx - r, icy - r, icx + r, icy + r), fill=VIOLET)
        ld.ellipse((icx - r, icy - r, icx + r, icy + r), outline=LILAC, width=3)
        ld.ellipse((icx - 11, icy - 11, icx + 11, icy + 11), fill=DEEP)
        ld.ellipse((icx - 7, icy - 9, icx + 1, icy), fill=WHITE)
        ld.ellipse((icx + 4, icy + 3, icx + 8, icy + 7), fill=LILAC)

    img.paste(layer, (0, 0), mask)

    d.arc((cx - rx + 1, top + 1, cx + rx - 1, cy + ry - 1), 10, 170, fill=DEEP, width=2)
    liner(d, cx, cy, rx, ry, open_ratio, out)
    if lashes_on:
        lashes(d, cx, cy, rx, ry, open_ratio, out, scale=lash_scale)


def closed_eye(d, cx, cy, happy=True, lash_scale=1.0):
    rx, ry = EYE_RX, EYE_RY
    out = -1 if cx < W / 2 else 1
    if happy:
        p0 = (cx - rx * 0.82, cy + 2)
        p2 = (cx + rx * 0.82, cy + 2)
        ctrl = (cx, cy - ry * 0.42)
    else:
        p0 = (cx - rx * 0.82, cy - 4)
        p2 = (cx + rx * 0.82, cy - 4)
        ctrl = (cx, cy + ry * 0.30)
    pts = bezier(p0, ctrl, p2, 16)
    stroke(d, pts[::-1] if out < 0 else pts, 4, 9, DEEP)
    # Lashes sit on the outer half of the closed lid and fan outwards.
    for i, length in enumerate((17.0, 24.0, 21.0)):
        bx, by = pts[i * 2] if out < 0 else pts[-1 - i * 2]
        ln = length * lash_scale
        tip = (bx + out * ln * 0.95, by - ln * 0.8)
        ctrl_lash = (bx + out * ln * 0.75, by - ln * 0.1)
        stroke(d, bezier((bx, by), ctrl_lash, tip), 6, 1, DEEP)


def tear(d, x, y, r=6, color=TEAR):
    d.ellipse((x - r, y - r, x + r, y + r), fill=color)
    d.polygon([(x - r * 0.7, y - r * 0.5), (x + r * 0.7, y - r * 0.5), (x, y - r * 2.1)], fill=color)


def drops(d, xs, phase, base_y=178, span=18):
    for i, x in enumerate(xs):
        y = base_y + ((phase + i * 5) % span)
        tear(d, x, y, 5 + (i % 2))


def zz(d, phase):
    for i in range(2):
        s = 12 + i * 7
        x = 186 - i * 10 + ((phase + i * 6) % 10)
        y = 60 - ((phase + i * 7) % 26) - i * 16
        for stroke in range(3):
            if stroke == 0:
                d.line([(x, y), (x + s, y)], fill=WHITE, width=3)
            elif stroke == 1:
                d.line([(x + s, y), (x, y + s)], fill=WHITE, width=3)
            else:
                d.line([(x, y + s), (x + s, y + s)], fill=WHITE, width=3)


def question(d, x, y):
    d.arc((x - 12, y - 26, x + 12, y + 2), 200, 20, fill=WHITE, width=4)
    d.line([(x + 8, y - 2), (x, y + 12)], fill=WHITE, width=4)
    d.ellipse((x - 3, y + 18, x + 3, y + 24), fill=WHITE)


def exclaim(d, x, y, double=False):
    d.line([(x, y - 22), (x, y + 6)], fill=WHITE, width=5)
    d.ellipse((x - 3, y + 12, x + 3, y + 18), fill=WHITE)
    if double:
        d.line([(x + 14, y - 22), (x + 14, y + 6)], fill=WHITE, width=5)
        d.ellipse((x + 11, y + 12, x + 17, y + 18), fill=WHITE)


def brow(d, cx, cy, tilt=0.0, color=DEEP):
    """A thin eyebrow; tilt moves the inner end down for angry/confident."""
    inner = cx + (18 if cx < W / 2 else -18)
    outer = cx + (-34 if cx < W / 2 else 34)
    mid = ((inner + outer) / 2, cy - 12)
    pts = [
        (inner, cy + tilt),
        (mid[0], mid[1]),
        (outer, cy + 2),
    ]
    d.line(pts, fill=color, width=4, joint="curve")


def blink_curve(frame, period, width=2):
    return frame % period < width


def finish(frames, out_dir, name):
    path = os.path.join(out_dir, name + ".gif")
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )
    return path


def neutral():
    frames = []
    for f in range(40):
        img, d = new_scene()
        blink = f in (10, 11, 30, 31)
        lookx = [0, 0, 0, -5, -6, -6, -4, 0, 0, 0, 5, 6, 6, 3, 0, 0, 0, 0, 0, 0][f % 20]
        looky = -2 if f % 20 in (3, 4, 5) else 0
        for cx in EYE_CX:
            if blink:
                closed_eye(d, cx, EYE_CY, happy=True)
            else:
                open_eye(img, d, cx, EYE_CY, 1.0, lookx, looky)
        frames.append(img)
    return frames


def happy():
    frames = []
    for f in range(32):
        bounce = round(6 * abs(math.sin(math.pi * f / 16)))
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY - bounce, 0.80, 0, 2)
        star(d, 34, 66 - bounce, 8 if f % 8 < 4 else 5, WHITE)
        star(d, 206, 54 - bounce, 6 if (f + 4) % 8 < 4 else 9, LILAC)
        blush(d, 34, 168)
        blush(d, 206, 168)
        frames.append(img)
    return frames


def laughing():
    frames = []
    for f in range(32):
        bounce = round(9 * abs(math.sin(math.pi * f / 8)))
        img, d = new_scene()
        for cx in EYE_CX:
            closed_eye(d, cx, EYE_CY - bounce, happy=True, lash_scale=1.15)
        star(d, 30 + (f % 4) * 2, 60 - bounce, 7, WHITE)
        star(d, 210 - (f % 4) * 2, 48 - bounce, 6, LILAC)
        star(d, 192, 78 - bounce, 4, WHITE)
        blush(d, 32, 172)
        blush(d, 208, 172)
        frames.append(img)
    return frames


def funny():
    frames = []
    for f in range(30):
        wiggle = 2 if f % 6 < 3 else -2
        img, d = new_scene()
        open_eye(img, d, EYE_CX[0], EYE_CY + wiggle, 0.95, -4, -3)
        closed_eye(d, EYE_CX[1], EYE_CY - wiggle, happy=True, lash_scale=1.2)
        star(d, 42, 56 + wiggle, 6, WHITE)
        frames.append(img)
    return frames


def sad():
    frames = []
    for f in range(36):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY + 3, 0.74, 0, 6)
        drops(d, [82, 158], f, base_y=176, span=30)
        frames.append(img)
    return frames


def angry():
    frames = []
    for f in range(30):
        img, d = new_scene()
        for i, cx in enumerate(EYE_CX):
            open_eye(img, d, cx, EYE_CY, 0.62, 0, 3)
            brow(d, cx, 56, tilt=6)
        # Anger marks (the anime cross that pops over an angry head).
        for i in range(4):
            x = 36 + (i % 2) * 8
            y = 54 + (i // 2) * 8
            d.line([(x, y), (x + 6, y + 6)], fill=LILAC, width=3)
            x = 204 - (i % 2) * 8
            d.line([(x, y), (x - 6, y + 6)], fill=LILAC, width=3)
        frames.append(img)
    return frames


def crying():
    frames = []
    for f in range(36):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY + 2, 0.55, 0, 4)
        drops(d, [78, 96, 146, 164], f, base_y=170, span=34)
        frames.append(img)
    return frames


def loving():
    frames = []
    for f in range(32):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY, 0.9, 0, 0, pupil="heart")
        for i in range(3):
            y = 74 - ((f + i * 9) % 34)
            heart(d, 44 + i * 76, y, 7 + (i % 2) * 2, PINK)
        blush(d, 32, 168)
        blush(d, 208, 168)
        frames.append(img)
    return frames


def embarrassed():
    frames = []
    for f in range(30):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY + 2, 0.8, -7, 4)
        blush(d, 30, 166)
        blush(d, 210, 166)
        tear(d, 202, 120 + (f % 10), 6)
        frames.append(img)
    return frames


def surprised():
    frames = []
    for f in range(26):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY - 2, 1.0, 0, 0, pupil="small")
        if f % 6 < 4:
            exclaim(d, 210, 60)
        frames.append(img)
    return frames


def shocked():
    frames = []
    for f in range(28):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY - 3, 1.0, 0, 0, pupil="small")
        if f % 4 < 2:
            exclaim(d, 196, 58, double=True)
        frames.append(img)
    return frames


def thinking():
    frames = []
    for f in range(30):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY - 2, 0.92, 7, -8)
        for i in range(3):
            r = 5 if (f // 3) % 3 == i else 3
            d.ellipse((198 + i * 14 - r, 60 - r, 198 + i * 14 + r, 60 + r),
                      fill=WHITE if (f // 3) % 3 == i else LILAC)
        frames.append(img)
    return frames


def winking():
    frames = []
    for f in range(30):
        img, d = new_scene()
        open_eye(img, d, EYE_CX[0], EYE_CY, 1.0, 4, -2)
        closed_eye(d, EYE_CX[1], EYE_CY, happy=True, lash_scale=1.3)
        for i in range(2):
            y = 66 - ((f + i * 12) % 26)
            heart(d, 206 - i * 16, y, 5, PINK)
        frames.append(img)
    return frames


def cool():
    frames = []
    for f in range(30):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY + 2, 0.55, -3, 2)
        star(d, 40, 58, 7 if f % 8 < 4 else 4, LILAC)
        star(d, 200, 48, 5 if f % 8 < 4 else 8, WHITE)
        frames.append(img)
    return frames


def relaxed():
    frames = []
    for f in range(40):
        img, d = new_scene()
        open_ratio = 0.66 + 0.04 * math.sin(2 * math.pi * f / 40)
        blink = blink_curve(f, 24, 2)
        for cx in EYE_CX:
            if blink:
                closed_eye(d, cx, EYE_CY, happy=True)
            else:
                open_eye(img, d, cx, EYE_CY, open_ratio, 0, 2)
        frames.append(img)
    return frames


def sleepy():
    frames = []
    for f in range(40):
        img, d = new_scene()
        t = f / 39
        open_ratio = 0.9 - 0.75 * (0.5 - 0.5 * math.cos(2 * math.pi * t))
        for cx in EYE_CX:
            if open_ratio < 0.2:
                closed_eye(d, cx, EYE_CY + 2, happy=False)
            else:
                open_eye(img, d, cx, EYE_CY + 2, open_ratio, 0, 5)
        zz(d, f)
        frames.append(img)
    return frames


def silly():
    frames = []
    for f in range(30):
        img, d = new_scene()
        open_eye(img, d, EYE_CX[0], EYE_CY, 0.95, 10, -2)
        open_eye(img, d, EYE_CX[1], EYE_CY, 0.95, -10, -2)
        star(d, 38, 54, 5 + (f % 4), WHITE)
        frames.append(img)
    return frames


def confident():
    frames = []
    for f in range(30):
        img, d = new_scene()
        for cx in EYE_CX:
            open_eye(img, d, cx, EYE_CY, 0.6, 2, 2)
        star(d, 204, 52, 7 if f % 6 < 3 else 4, WHITE)
        frames.append(img)
    return frames


def confused():
    frames = []
    for f in range(32):
        img, d = new_scene()
        open_eye(img, d, EYE_CX[0], EYE_CY, 0.95, 5, -4)
        open_eye(img, d, EYE_CX[1], EYE_CY, 0.62, -4, 2)
        question(d, 204, 54)
        frames.append(img)
    return frames


def delicious():
    frames = []
    for f in range(30):
        img, d = new_scene()
        bounce = round(3 * abs(math.sin(math.pi * f / 15)))
        for cx in EYE_CX:
            closed_eye(d, cx, EYE_CY - bounce, happy=True, lash_scale=1.1)
        heart(d, 196, 62 - bounce, 7, PINK)
        heart(d, 48, 70 - bounce, 5, PINK)
        blush(d, 34, 168)
        blush(d, 206, 168)
        frames.append(img)
    return frames


def kissy():
    frames = []
    for f in range(30):
        img, d = new_scene()
        for cx in EYE_CX:
            closed_eye(d, cx, EYE_CY, happy=True, lash_scale=1.2)
        y = 58 - ((f * 2) % 24)
        heart(d, 200, y, 8, PINK)
        heart(d, 214, y + 12, 4, PINK)
        blush(d, 32, 168)
        blush(d, 208, 168)
        frames.append(img)
    return frames


EMOTIONS = {
    "angry": angry,
    "confident": confident,
    "confused": confused,
    "cool": cool,
    "crying": crying,
    "delicious": delicious,
    "embarrassed": embarrassed,
    "funny": funny,
    "happy": happy,
    "kissy": kissy,
    "laughing": laughing,
    "loving": loving,
    "neutral": neutral,
    "relaxed": relaxed,
    "sad": sad,
    "shocked": shocked,
    "silly": silly,
    "sleepy": sleepy,
    "surprised": surprised,
    "thinking": thinking,
    "winking": winking,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    total = 0
    for name, builder in sorted(EMOTIONS.items()):
        frames = builder()
        path = finish(frames, args.out, name)
        size = os.path.getsize(path)
        total += size
        print(f"{name:12s} {len(frames):3d} frames {size:7d} B")
    print(f"\n{len(EMOTIONS)} animations, {total} B ({total / 1024:.0f} KiB)")


if __name__ == "__main__":
    main()
