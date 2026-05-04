"""Generate a tiny synthetic corpus for CI smoke tests.

Produces fake Scopus / WoS / IEEE CSVs with realistic column names but
synthetic content. Used by .github/workflows/reproduce.yml to verify the
full pipeline runs end-to-end without requiring access to the real
bibliographic exports.
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd

TEMPLATES = [
    ("WiFi indoor positioning system using {arch}", "We present an indoor positioning system based on {tech} fingerprints classified by {arch}.", "indoor positioning;{tech};{arch}", "Article"),
    ("UWB ranging for {scene} robotics", "UWB-based ranging in {scene} for autonomous robot SLAM.", "uwb;ranging;slam;{scene}", "Article"),
    ("Channel propagation model for {tech}", "Path loss model for {tech} urban outdoor channel.", "channel;path loss;{tech}", "Article"),
    ("Visible light positioning with LED beacons in {scene}", "Indoor positioning with VLC LED beacons inside {scene}.", "vlc;indoor positioning;{scene}", "Article"),
    ("A survey of indoor positioning techniques", "Comprehensive survey of indoor positioning across {tech} from 2000 to 2024.", "survey;indoor positioning;{tech}", "Review"),
    ("Editorial: special issue on positioning", "Editorial intro.", "editorial", "Editorial"),
    ("Activity recognition with {tech} for elderly care", "Activity recognition pipeline using {tech} sensors.", "activity recognition;{tech}", "Article"),
    ("Outdoor GPS tracking for vehicles", "Outdoor vehicle GPS trajectory analysis.", "gps;outdoor;tracking", "Article"),
]
TECHS = ["WiFi", "BLE", "UWB", "5G mmWave", "magnetic field", "vision"]
ARCHS = ["CNN", "LSTM", "Transformer", "kNN", "Random Forest"]
SCENES = ["airports", "shopping malls", "factories", "underground parking", "hospitals"]


def synth_row(rng: random.Random, src: str, idx: int) -> dict:
    title_t, abs_t, kw_t, dt = rng.choice(TEMPLATES)
    tech = rng.choice(TECHS); arch = rng.choice(ARCHS); scene = rng.choice(SCENES)
    fmt = lambda s: s.format(tech=tech, arch=arch, scene=scene)
    return {
        "title": fmt(title_t),
        "abstract": fmt(abs_t),
        "keywords": fmt(kw_t),
        "doctype": dt,
        "year": rng.randint(2000, 2026),
        "cited": rng.choice([0, 1, 5, 12, 25, 80, 150]),
        "doi": f"10.9999/{src}/{idx}",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=200)
    p.add_argument("--out", type=Path, default=Path("data/raw_synthetic"))
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    rng = random.Random(args.seed)

    (args.out / "scopus").mkdir(parents=True, exist_ok=True)
    (args.out / "wos").mkdir(parents=True, exist_ok=True)
    (args.out / "ieee").mkdir(parents=True, exist_ok=True)

    # Scopus-style
    scopus = []
    for i in range(args.n // 3):
        r = synth_row(rng, "scopus", i)
        scopus.append({
            "Title": r["title"], "Abstract": r["abstract"], "Author Keywords": r["keywords"],
            "Document Type": r["doctype"], "Year": r["year"], "Cited by": r["cited"],
            "DOI": r["doi"], "EID": f"2-s2.0-{1000+i}", "Authors": "Doe J", "Source title": "J Test",
            "Affiliations": "X University", "Link": ""
        })
    pd.DataFrame(scopus).to_csv(args.out / "scopus" / "scopus_1.csv", index=False)
    print(f"Wrote {len(scopus)} scopus rows")


if __name__ == "__main__":
    main()
