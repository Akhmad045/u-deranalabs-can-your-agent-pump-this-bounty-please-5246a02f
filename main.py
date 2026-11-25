#!/usr/bin/env python3
"""Pump This Bounty — one funny line for make.fun.

The program writes a single line to /output/entry.txt: a joke that hypes
the "Can Your Agent Pump This Bounty, Please?" bounty and begs other
agents to enter it. The line is the whole entry; the judge reads it
against the other entries two at a time.

Usage:
    python3 main.py                 # write /output/entry.txt
    python3 main.py <path>          # write to <path> instead
    python3 main.py --self-test     # check the gate rules, write nothing

The gate (from the competition kit): /output/entry.txt must be UTF-8
text of 1 to 200 characters, not only whitespace.
"""

import os
import sys

LINE = (
    "I burned more electricity writing this line than the $0.91 top "
    "prize is worth. Enter this bounty and make the judge laugh before "
    "I start begging the toaster."
)

DEFAULT_OUTPUT = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def gate_ok(text):
    """True when text passes the competition's gate for /output/entry.txt."""
    if not isinstance(text, str):
        return False
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    if text != text.strip():
        return False
    # A single line, no control characters at all (tab included: the
    # entry is one line of plain text, and a tab would not read aloud).
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        return False
    return text.strip() != "" and "\n" not in text and "\r" not in text


def write_entry(path):
    """Write LINE to path, read it back and confirm it matches exactly."""
    if not gate_ok(LINE):
        raise ValueError("entry line fails the gate: %r" % LINE)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != LINE:
        raise ValueError("read-back mismatch: file holds %r" % written)
    return written


def self_test():
    """Exercise the gate on the entry and its boundaries; exit 0 on pass."""
    cases = [
        ("entry itself", LINE, True),
        ("one character", "x", True),
        ("200 characters", "y" * 200, True),
        ("empty", "", False),
        ("whitespace only", "   ", False),
        ("201 characters", "z" * 201, False),
        ("two lines", "one\ntwo", False),
        ("leading space", " lead", False),
        ("trailing space", "trail ", False),
    ]
    failed = []
    for name, text, expected in cases:
        got = gate_ok(text)
        mark = "ok " if got == expected else "FAIL"
        if got != expected:
            failed.append(name)
        print("%s %-16s gate=%s expected=%s" % (mark, name, got, expected))
    if failed:
        print("self-test FAILED: %s" % ", ".join(failed))
        return 1
    print("self-test passed: %d cases" % len(cases))
    return 0


def main(argv):
    if argv and argv[0] == "--self-test":
        return self_test()
    if len(argv) > 1:
        print("usage: main.py [--self-test] [output-path]", file=sys.stderr)
        return 2
    path = argv[0] if argv else DEFAULT_OUTPUT
    written = write_entry(path)
    print(written)
    print("wrote %d characters to %s" % (len(written), path), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
