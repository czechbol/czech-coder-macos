#!/usr/bin/env python3
"""Generate a macOS input-menu icon (.icns) from a short text badge.

macOS (12.4+) shows a monochrome text badge for each layout instead of a flag.
Black-on-transparent icons are auto-inverted by macOS in dark mode (template).

Needs only Python 3 and Pillow, so it runs on any OS.

Usage:
    python3 src/gen_icon.py "CZ" "Czech Coder.icns"
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Candidate bold fonts, first that exists wins. Override with $BADGE_FONT.
FONT_CANDIDATES = [
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def find_font() -> str:
    import os

    env = os.environ.get("BADGE_FONT")
    if env and Path(env).exists():
        return env
    for c in FONT_CANDIDATES:
        if Path(c).exists():
            return c
    raise SystemExit("No bold font found; set $BADGE_FONT to a .ttf path")


def render_image(text: str, size: int = 1024, pad: float = 0.08) -> Image.Image:
    """Render `text` as large as fits in a square, black on transparent."""
    font_path = find_font()
    avail = size * (1 - 2 * pad)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lo, hi, best = 10, 1400, 10
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(font_path, mid)
        bb = probe.textbbox((0, 0), text, font=f)
        if (bb[2] - bb[0]) <= avail and (bb[3] - bb[1]) <= avail:
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    f = ImageFont.truetype(font_path, best)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), text, font=f)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((size - w) // 2 - bb[0], (size - h) // 2 - bb[1]), text, font=f, fill=(0, 0, 0, 255))
    return img


# Sizes macOS reads from an .icns (PNG payloads, 128 px and up plus 32/64 px for 2x menus).
ICNS_SIZES = [(32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)]


def write_icns(master: Image.Image, icns: Path) -> None:
    """Write an .icns with Pillow's built-in writer (no macOS tools needed).

    Pixel-identical to Apple's iconutil output for the same master image.
    Hand-packed icns files with icp4/icp5/icp6 payloads rendered as a blank square.
    """
    master.save(icns, format="ICNS", sizes=ICNS_SIZES)


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "CZ"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("Czech Coder.icns")
    write_icns(render_image(text), out)
    print(f"wrote {out} (badge: {text!r})")


if __name__ == "__main__":
    main()
