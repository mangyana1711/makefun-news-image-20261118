"""makefun-news-image-20261118: an illustrated front page summing up
Wednesday 18 November 2026 world news — 33 stories, 6 continents,
one world map.

The program is deterministic and offline: it base64-decodes the
entry image bundled in this repository (entry.png.b64) and writes
it to the output path. It runs under the make.fun sandbox with no
network access and must produce identical bytes on every run.
"""

import base64
import os
import sys
from pathlib import Path

# PNG signature: the first eight bytes of every PNG file.
PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

# The image must fit make.fun's 1 MiB entry limit.
MAX_SIZE = 1024 * 1024


def resolve_output() -> Path:
    """Pick the output path for entry.png.

    The make.fun harness sets MAKEFUN_OUTPUT_DIR; the sandbox also
    provides /output. Locally, fall back to the current directory.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        return Path(out_dir) / "entry.png"
    if Path("/output").is_dir():
        return Path("/output/entry.png")
    return Path("entry.png")


def main() -> int:
    here = Path(__file__).resolve().parent
    b64_path = here / "entry.png.b64"
    raw = b64_path.read_bytes()
    try:
        png = base64.b64decode(raw, validate=True)
    except Exception as exc:
        print(f"error: entry.png.b64 is not valid base64: {exc}", file=sys.stderr)
        return 1
    if len(png) < len(PNG_MAGIC) or png[:8] != PNG_MAGIC:
        print("error: decoded data is not a PNG file", file=sys.stderr)
        return 1
    if len(png) > MAX_SIZE:
        print(f"error: PNG is {len(png)} bytes, over the 1048576-byte limit", file=sys.stderr)
        return 1
    # A complete PNG ends with the 12-byte IEND chunk (zero length, type
    # "IEND", CRC 0xAE426082). A truncated image would still pass the
    # magic check above, so verify the trailer too.
    iend = bytes([0, 0, 0, 0, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82])
    if len(png) < 12 or png[-12:] != iend:
        print("error: PNG is truncated (missing IEND trailer)", file=sys.stderr)
        return 1
    out = resolve_output()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(png)
    print(f"wrote {out} ({len(png)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
