#!/usr/bin/env python3
"""Draw one image that sums up the world news of Tuesday 24 November 2026.

Standard library only. The picture is rendered pixel by pixel from fixed
data, so every run writes exactly the same bytes to /output/entry.png.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 227)
INK = (32, 36, 46)
RED = (179, 49, 42)
NAVY = (39, 65, 86)
SEA = (127, 168, 184)
DEEP = (62, 107, 126)
SAND = (217, 201, 163)
GREY = (110, 116, 124)
WHITE = (252, 250, 244)
FLAME = (232, 119, 44)
YELLOW = (240, 190, 60)

# ------------------------------------------------------------- 5x7 font
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", ".#.#.", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", "..#..", ".....", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#.##", "#..##"),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
}

# ------------------------------------------------------------- canvas
PX = bytearray(W * H * 3)


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        PX[i] = c[0]
        PX[i + 1] = c[1]
        PX[i + 2] = c[2]


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            put(xx, yy, c)


def frame(x, y, w, h, t, c):
    rect(x, y, w, t, c)
    rect(x, y + h - t, w, t, c)
    rect(x, y, t, h, c)
    rect(x + w - t, y, t, h, c)


def circle(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                put(xx, yy, c)


def ring(cx, cy, r, t, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
            if (r - t) * (r - t) <= d <= r * r:
                put(xx, yy, c)


def line(x0, y0, x1, y1, t, c):
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    for s in range(steps + 1):
        x = x0 + (x1 - x0) * s // steps
        y = y0 + (y1 - y0) * s // steps
        for dy in range(-(t // 2), t - t // 2):
            for dx in range(-(t // 2), t - t // 2):
                put(x + dx, y + dy, c)


def text_w(s, scale, track):
    return len(s) * (5 * scale + track) - track


def draw_text(x, y, s, scale, c, track=None):
    if track is None:
        track = scale
    cx = x
    for ch in s.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == "#":
                    rect(cx + col * scale, y + row * scale, scale, scale, c)
        cx += 5 * scale + track
    return cx - track


def centered(y, s, scale, c, track=None):
    if track is None:
        track = scale
    x = (W - text_w(s, scale, track)) // 2
    return draw_text(x, y, s, scale, c, track)


def wrap(s, scale, max_w, track=None):
    if track is None:
        track = scale
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if text_w(trial, scale, track) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def block(x, y, s, scale, c, max_w, leading=None, center=False):
    if leading is None:
        leading = 7 * scale + scale * 2
    for ln in wrap(s, scale, max_w):
        if center:
            draw_text(x + (max_w - text_w(ln, scale, scale)) // 2, y, ln, scale, c)
        else:
            draw_text(x, y, ln, scale, c)
        y += leading
    return y


# ------------------------------------------------------------- scenes
def tanker_scene(x, y, w, h):
    """Strait of Hormuz: a tanker afire, an escort, mines in the water."""
    rect(x, y, w, h, SEA)
    rect(x, y, w, 26, NAVY)                       # sky band
    rect(x, y + h - 30, w, 30, DEEP)              # deep water band
    for i in range(9):                            # wave dashes
        rect(x + 24 + i * 62, y + h - 58, 30, 5, WHITE)
        rect(x + 54 + i * 62, y + 44, 26, 5, WHITE)
    # escort ship, left
    rect(x + 30, y + 96, 120, 16, GREY)
    rect(x + 58, y + 78, 44, 18, GREY)
    rect(x + 76, y + 58, 8, 20, INK)
    line(x + 34, y + 112, x + 146, y + 112, 5, INK)
    # tanker hull, centre-right
    rect(x + 205, y + 92, 330, 26, RED)
    rect(x + 205, y + 118, 330, 8, INK)
    for i in range(6):                            # deck tanks
        rect(x + 222 + i * 42, y + 74, 32, 18, SAND)
    rect(x + 486, y + 52, 34, 40, WHITE)          # bridge tower
    rect(x + 494, y + 60, 18, 10, NAVY)
    # flames and smoke on the tanker
    circle(x + 300, y + 58, 17, FLAME)
    circle(x + 322, y + 48, 12, YELLOW)
    circle(x + 282, y + 50, 10, YELLOW)
    circle(x + 306, y + 26, 13, GREY)
    circle(x + 330, y + 16, 10, GREY)
    # mines in the water
    for mx, my in ((x + 180, y + 150), (x + 420, y + 158), (x + 520, y + 138)):
        circle(mx, my, 11, INK)
        for dx, dy in ((0, -16), (11, -11), (16, 0), (11, 11),
                       (0, 16), (-11, 11), (-16, 0), (-11, -11)):
            line(mx, my, mx + dx, my + dy, 3, INK)


def court_icon(cx, y):
    """A courthouse: pediment, columns, steps. About 78 px tall."""
    for i in range(8):                            # pediment
        rect(cx - 48 + i * 6, y + i * 2, 96 - i * 12, 4, NAVY)
    rect(cx - 52, y + 18, 104, 6, NAVY)
    for i in range(4):                            # columns
        rect(cx - 42 + i * 26, y + 28, 9, 34, NAVY)
    rect(cx - 52, y + 66, 104, 6, NAVY)
    rect(cx - 58, y + 74, 116, 6, NAVY)


def corvette_icon(cx, y):
    """A warship with a naval drone above it. About 74 px tall."""
    # drone: body, arms, rotors
    rect(cx - 11, y - 2, 22, 7, RED)
    line(cx - 24, y - 8, cx + 24, y + 6, 3, INK)
    line(cx - 24, y + 6, cx + 24, y - 8, 3, INK)
    for dx in (-28, 28):
        rect(cx + dx - 8, y - 12, 16, 4, INK)
        rect(cx + dx - 8, y + 8, 16, 4, INK)
    # ship
    rect(cx - 28, y + 34, 48, 15, NAVY)           # superstructure
    rect(cx - 5, y + 20, 6, 14, INK)              # mast
    rect(cx + 24, y + 40, 24, 5, INK)             # gun
    rect(cx - 60, y + 52, 120, 13, NAVY)          # hull
    line(cx - 60, y + 68, cx + 60, y + 68, 4, INK)


def aden_icon(cx, y):
    """A coastline, an advance arrow, a port flag. About 84 px tall."""
    rect(cx - 60, y - 8, 120, 92, SAND)           # land
    rect(cx - 60, y + 56, 120, 28, SEA)           # sea strip
    for i in range(4):
        rect(cx - 48 + i * 28, y + 66, 15, 4, WHITE)
    line(cx - 42, y + 38, cx + 18, y + 4, 7, RED)  # advance arrow shaft
    line(cx + 18, y + 4, cx, y + 2, 6, RED)        # arrow head
    line(cx + 18, y + 4, cx + 20, y + 22, 6, RED)
    rect(cx + 32, y - 4, 5, 36, INK)              # flag pole
    rect(cx + 37, y - 4, 24, 15, RED)             # flag
    circle(cx + 42, y + 72, 6, NAVY)              # port marker


# ------------------------------------------------------------- page
def build():
    rect(0, 0, W, H, PAPER)
    frame(16, 16, W - 32, H - 32, 4, INK)
    frame(28, 28, W - 56, H - 56, 2, INK)

    # masthead
    centered(52, "THE WORLD IN ONE IMAGE", 4, NAVY, track=8)
    centered(96, "TUESDAY", 5, RED, track=14)
    centered(146, "24 NOVEMBER 2026", 10, INK)
    rect(64, 232, W - 128, 4, INK)
    rect(64, 242, W - 128, 2, INK)

    # lead story: Hormuz
    tanker_scene(64, 262, W - 128, 208)
    frame(64, 262, W - 128, 208, 3, INK)
    block(64, 490, "IRAN SAYS TANKERS HIT MINES IN HORMUZ", 6, INK,
          W - 128, leading=54, center=True)
    block(104, 606,
          "TEHRAN SAYS THREE OIL TANKERS STRUCK NAVAL MINES AND CAUGHT "
          "FIRE UNDER US ESCORT. WASHINGTON HAS NOT CONFIRMED THE CLAIM.",
          3, NAVY, W - 208, leading=28, center=True)

    rect(64, 692, W - 128, 3, INK)

    # three panels: icon band 712-792, headline 800-864, body 872-948
    cols = (64, 368, 672)
    for cx in cols:
        frame(cx, 704, 288, 254, 2, GREY)
    court_icon(cols[0] + 144, 712)
    corvette_icon(cols[1] + 144, 724)
    aden_icon(cols[2] + 144, 714)
    block(cols[0] + 16, 800, "HUAWEI CONVICTED", 4, INK, 256,
          leading=36, center=True)
    block(cols[0] + 16, 876,
          "US JURY: GUILTY ON 10 OF 12 COUNTS - FRAUD, SANCTIONS AND "
          "TRADE-SECRETS THEFT.",
          2, NAVY, 256, leading=19, center=True)
    block(cols[1] + 16, 800, "UKRAINE DEFENDS", 4, INK, 256,
          leading=36, center=True)
    block(cols[1] + 16, 876,
          "CITES SELF-DEFENCE AFTER NAVAL DRONES SANK A RUSSIAN "
          "CORVETTE IN LIBYA.",
          2, NAVY, 256, leading=19, center=True)
    block(cols[2] + 16, 800, "HOUTHIS NEAR ADEN", 4, INK, 256,
          leading=36, center=True)
    block(cols[2] + 16, 876,
          "FIGHTERS ADVANCE TO 60 KM FROM ADEN, YEMEN'S GOVERNMENT "
          "SEAT, ARMY SAYS.",
          2, NAVY, 256, leading=19, center=True)

    rect(64, 970, W - 128, 2, INK)
    centered(978, "REPORTED BY REUTERS, AP AND CNN", 2, GREY)


def main():
    build()
    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        start = yy * W * 3
        raw += PX[start:start + W * 3]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        return out + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)


if __name__ == "__main__":
    main()
