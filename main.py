#!/usr/bin/env python3
"""make.fun entry: 18 November 2026 world news in one image (v3).

Decodes the bundled front-page image (entry.png.b64) and writes it as
entry.png. The front page sums up Wednesday 18 November 2026: 33 stories
across 6 continents, with 9 illustrated features, a world map, a
"BY THE NUMBERS" strip and an "ALSO ON ..." list. Stdlib only, no network.
"""
import base64
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B64_PATH = os.path.join(HERE, "entry.png.b64")
MAX_BYTES = 1024 * 1024  # the image itself must stay under 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_path():
    """Where the image goes: MAKEFUN_OUTPUT_DIR, else /output, else here."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return os.path.join(env_dir, "entry.png")
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return os.path.join(HERE, "entry.png")


def main():
    # Fail fast: base64 expands data by ~4/3, so a bundle over ~1.4 MB
    # cannot decode within the 1 MiB image limit. Check before decoding.
    b64_size = os.path.getsize(B64_PATH)
    if b64_size > MAX_BYTES * 4 // 3 + 8:
        print("entry.png.b64 is %d bytes; too large to decode under 1 MiB"
              % b64_size, file=sys.stderr)
        return 1
    with open(B64_PATH, "r", encoding="ascii") as f:
        encoded = f.read().strip()
    try:
        data = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        print("entry.png.b64 is not valid base64: %s" % exc, file=sys.stderr)
        return 1
    if not data.startswith(PNG_MAGIC):
        print("decoded payload is not a PNG", file=sys.stderr)
        return 1
    if not 0 < len(data) <= MAX_BYTES:
        print("decoded PNG is %d bytes (limit %d)" % (len(data), MAX_BYTES),
              file=sys.stderr)
        return 1
    out = output_path()
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
