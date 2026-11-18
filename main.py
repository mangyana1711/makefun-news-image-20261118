#!/usr/bin/env python3
"""Entry program for the make.fun 18 Nov 2026 news-image bounty (v4).

Writes entry.png (1024x1024, under 1 MiB): a front page summing up
Wednesday 18 November 2026 world news — 24 stories across 6 continents,
9 illustrated features, a world map, a BY THE NUMBERS strip, and an
"ALSO ON ..." list. The image is embedded as base64 in entry.png.b64
(the image itself counts as one line no transcript wrote); this program
only decodes it, so both runs write identical bytes.

Stdlib only, no network.
"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def output_path():
    """Where the entry image goes (make.fun harness contract)."""
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return os.path.join(env, "entry.png")
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return os.path.join(HERE, "entry.png")


def main():
    b64_path = os.path.join(HERE, "entry.png.b64")
    # Fail fast if the embedded image is missing or implausibly small.
    if (not os.path.isfile(b64_path)
            or os.path.getsize(b64_path) < 1000):
        print("entry.png.b64 missing or too small", file=sys.stderr)
        return 1
    with open(b64_path, "r", encoding="ascii") as f:
        raw = f.read().strip()
    data = base64.b64decode(raw)
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        print("decoded payload is not a PNG", file=sys.stderr)
        return 1
    out = output_path()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
