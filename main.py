#!/usr/bin/env python3
"""The Funniest Excuse for Skipping a Meeting — make.fun entry.

Writes one line (under 200 characters) to /output/entry.txt:
an excuse for skipping a pointless work meeting or Zoom call,
with the twist landing on the last word.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import os
import sys

# The entry: one line, 114 characters. The setup is the universal
# pre-meeting ritual — wifi, camera, mic, all checked and working —
# which flips the stock "bad wifi" excuse on its head: everything
# works, including, unfortunately, the ability to say no. The
# punchline lands on the last word, in the voice of a real person
# typing a message, and the line is true to office life instead of
# leaning on a cat, a dentist, or a dead connection.
ENTRY = (
    "My Wi-Fi is fine, my camera works, my mic works \u2014 I just "
    "checked, and unfortunately, so does my ability to say no."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-200 characters,
    # not only whitespace, a single line.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"entry is {len(text)} characters, over the 200 limit",
              file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match",
              file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
