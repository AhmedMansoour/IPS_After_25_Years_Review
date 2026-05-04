"""Verify SHA-256 hashes of pipeline outputs against config/expected_hashes.txt.

Format of expected_hashes.txt (one entry per line):
    <sha256>  <relative_path>
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    expected_path = Path("config/expected_hashes.txt")
    if not expected_path.exists():
        print(f"NOTE: {expected_path} does not exist yet.")
        print("After your first verified pipeline run, populate it with `make freeze-hashes`.")
        return 0

    failed = 0
    for line in expected_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sha, rel = line.split(maxsplit=1)
        target = Path(rel)
        if not target.exists():
            print(f"MISSING  {rel}")
            failed += 1
            continue
        got = sha256(target)
        ok = got == sha
        print(f"{'OK     ' if ok else 'MISMATCH'}  {rel}  (got {got[:16]}...)")
        if not ok:
            failed += 1

    if failed:
        print(f"\n{failed} hash check(s) failed.", file=sys.stderr)
        return 1
    print("\nAll hashes match. Reproduction is bit-identical.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
