#!/usr/bin/env python3
"""Generate a macOS input-menu icon (.icns) from a short text badge.

macOS (12.4+) shows a monochrome text badge for each layout instead of a flag.
Black-on-transparent icons are auto-inverted by macOS in dark mode (template).

Writes a real PNG-based .icns with no external tools (pure Pillow + stdlib).

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


# icns OSType -> pixel size. PNG payloads are accepted for these since OS X 10.7.
ICNS_TYPES = [
    (b"icp4", 16), (b"icp5", 32), (b"icp6", 64),
    (b"ic07", 128), (b"ic08", 256), (b"ic09", 512), (b"ic10", 1024),
    (b"ic11", 32), (b"ic12", 64), (b"ic13", 256), (b"ic14", 512),
]


def write_icns(master: Image.Image, icns: Path) -> None:
    """Pack a real PNG-based .icns directly (no external tools).

    ImageMagick on Linux lacks an icns encoder and silently writes a PNG with
    an .icns name, which macOS can't parse and crashes the input-source picker.
    """
    import io
    import struct

    entries = []
    for ostype, px in ICNS_TYPES:
        buf = io.BytesIO()
        master.resize((px, px), Image.LANCZOS).save(buf, format="PNG")
        data = buf.getvalue()
        entries.append(ostype + struct.pack(">I", len(data) + 8) + data)
    body = b"".join(entries)
    with open(icns, "wb") as fh:
        fh.write(b"icns" + struct.pack(">I", len(body) + 8) + body)


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "CZ"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("Czech Coder.icns")
    write_icns(render_image(text), out)
    print(f"wrote {out} (badge: {text!r})")


if __name__ == "__main__":
    main()
