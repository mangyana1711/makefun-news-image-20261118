#!/usr/bin/env python3
"""make.fun entry: Sum up 18 November's world news in one image.

Writes the entry image to the output directory. The image bytes live in
entry.png.b64 (base64 of entry.png) next to this file; this program just
decodes them, so both runs produce identical bytes.
"""
import base64
import os
import pathlib
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = pathlib.Path(__file__).resolve().parent
    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    text = (here / "entry.png.b64").read_text().strip()
    data = base64.b64decode(text, validate=True)
    if not data.startswith(PNG_MAGIC):
        print("entry.png.b64 does not decode to a PNG", file=sys.stderr)
        raise SystemExit(1)
    (out_dir / "entry.png").write_bytes(data)


if __name__ == "__main__":
    main()
