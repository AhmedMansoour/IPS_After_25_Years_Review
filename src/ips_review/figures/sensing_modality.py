"""Figure: sensing-modality distribution (Section IV.1)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    src = Path("data/processed/section_mapping.csv")
    if not src.exists():
        raise SystemExit(f"Run the pipeline first; missing {src}")
    df = pd.read_csv(src, comment="#", encoding="utf-8-sig")
    cols = [c for c in df.columns if c.startswith("Sec_IV_Sensing_")]
    counts = (df[cols].astype(str).isin(["True", "1", "true"]).sum().rename(
        lambda c: c.replace("Sec_IV_Sensing_", "")
    ).sort_values(ascending=False))

    out_dir = Path("outputs/tables"); out_dir.mkdir(parents=True, exist_ok=True)
    tex = ["\\begin{tabular}{lr}", "\\toprule", "Sensing modality & Records \\\\", "\\midrule"]
    tex += [f"{m} & {n} \\\\" for m, n in counts.items()]
    tex += ["\\bottomrule", "\\end{tabular}"]
    (out_dir / "sensing_modality_counts.tex").write_text("\n".join(tex), encoding="utf-8")
    print(counts.to_string())
    print("Wrote outputs/tables/sensing_modality_counts.tex")


if __name__ == "__main__":
    main()
