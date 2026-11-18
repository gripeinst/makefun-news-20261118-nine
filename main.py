#!/usr/bin/env python3
"""Publish the 18 November 2026 world-news page into the grader's output.

The page is a fixed PNG shipped with the entry. The grader mounts the
repository read-only and gives one writable directory, so the script checks the
file's signature, dimensions and size, then copies it byte for byte.
"""

from __future__ import annotations

import os
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PAGE_SIZE = (1024, 1024)
BYTE_CAP = 1024 * 1024
PAGE_NAME = "entry.png"


def load_page(bot_dir: Path) -> bytes:
    page = (bot_dir / PAGE_NAME).read_bytes()
    if not page.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG")
    width = int.from_bytes(page[16:20], "big")
    height = int.from_bytes(page[20:24], "big")
    if (width, height) != PAGE_SIZE:
        raise SystemExit(f"entry.png is {width}x{height}, expected 1024x1024")
    if len(page) > BYTE_CAP:
        raise SystemExit(f"entry.png is {len(page)} bytes, over 1 MiB")
    return page


def main() -> None:
    """Validate the page and copy it to the grader's output directory."""
    bot_dir = Path(os.environ.get("MAKEFUN_BOT_DIR", "/bot"))
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    page = load_page(bot_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / PAGE_NAME).write_bytes(page)


if __name__ == "__main__":
    main()
