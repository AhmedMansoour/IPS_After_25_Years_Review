"""Fail-closed SHA-256 output verification.

Requires a nonempty version-controlled config/expected_hashes.txt.
This program cannot pass in the absence of verification references.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    expected_path = Path("config/expected_hashes.txt")
    if not expected_path.is_file():
        print("FAIL: missing config/expected_hashes.txt; results not hash-verified.", file=sys.stderr)
        return 1
    checks = [
        line.strip() for line in expected_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not checks:
        print("FAIL: expected-hashes manifest is empty.", file=sys.stderr)
        return 1
    errors = 0
    for item in checks:
        parts = item.split(maxsplit=1)
        if len(parts) != 2 or len(parts[0]) != 64:
            print(f"FAIL: malformed manifest line: {item}", file=sys.stderr)
            errors += 1
            continue
        expected, name = parts
        path = Path(name)
        if not path.is_file():
            print(f"FAIL: missing {name}", file=sys.stderr)
            errors += 1
        elif sha256(path) != expected:
            print(f"FAIL: hash mismatch for {name}", file=sys.stderr)
            errors += 1
        else:
            print(f"PASS: {name}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
