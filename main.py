#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — make.fun entry.

Writes one original haiku about debugging (5-7-5 syllables, three lines)
to /output/entry.txt. Deterministic, no network, no randomness.

Chosen haiku (written by hand for this bounty; see CANDIDATES.md for the
three candidates considered and why this one won):

    Cursor blinks at three
    the log repeats one red line
    the typo was mine

Syllable counts, verified by hand:
    Line 1: Cur-sor(2) blinks(1) at(1) three(1)            = 5
    Line 2: the(1) log(1) re-peats(2) one(1) red(1) line(1) = 7
    Line 3: the(1) ty-po(2) was(1) mine(1)                 = 5

Total length including newlines: 70 characters (limit 200).
"""

import os
import sys

HAIKU = (
    "Cursor blinks at three\n"
    "the log repeats one red line\n"
    "the typo was mine\n"
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text: str) -> None:
    """Guard the gate before writing: UTF-8, 1-200 chars, not blank,
    exactly three non-empty lines."""
    if not text or not text.strip():
        raise ValueError("haiku is empty or only whitespace")
    if "\r" in text:
        raise ValueError("haiku must use LF line endings only, no CR")
    if not text.endswith("\n") or text.endswith("\n\n"):
        raise ValueError("haiku must end with exactly one trailing newline")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"haiku is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku must be exactly 3 lines, got {len(lines)}")
    if any(not line.strip() for line in lines):
        raise ValueError("haiku has a blank line")


def main() -> int:
    validate(HAIKU)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(HAIKU)
    os.chmod(OUTPUT_PATH, 0o644)
    # Confirm what landed on disk, so a silent write failure cannot pass.
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    if raw.decode("utf-8") != HAIKU:
        raise ValueError("verification failed: file content differs from haiku")
    if len(raw) > MAX_CHARS:
        raise ValueError("verification failed: file exceeds 200 bytes")
    print(f"Wrote {len(HAIKU)} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
