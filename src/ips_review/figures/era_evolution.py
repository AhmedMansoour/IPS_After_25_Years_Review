"""Figure: era evolution (Section III).

Reads data/processed/section_mapping.csv and produces:
    outputs/figures/era_evolution.pdf
    outputs/tables/era_counts.tex
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    src = Path("data/processed/section_mapping.csv")
    if not src.exists():
        raise SystemExit(f"Run the pipeline first; missing {src}")
    df = pd.read_csv(src, comment="#", encoding="utf-8-sig")
    counts = df["Sec_III_Era"].value_counts().reindex(["Era1", "Era2", "Era3", "Era4"]).fillna(0).astype(int)
    out_dir = Path("outputs/tables"); out_dir.mkdir(parents=True, exist_ok=True)

    tex = ["\\begin{tabular}{lr}", "\\toprule", "Era & Records \\\\", "\\midrule"]
    tex += [f"{e} & {n} \\\\" for e, n in counts.items()]
    tex += ["\\bottomrule", "\\end{tabular}"]
    (out_dir / "era_counts.tex").write_text("\n".join(tex), encoding="utf-8")
    print(counts.to_string())
    print(f"Wrote outputs/tables/era_counts.tex")

    try:
        import matplotlib.pyplot as plt
        fig_dir = Path("outputs/figures"); fig_dir.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.bar(counts.index, counts.values)
        ax.set_ylabel("Retained records")
        ax.set_title("Era distribution (I-Core + I-Context)")
        fig.tight_layout()
        fig.savefig(fig_dir / "era_evolution.pdf")
        print("Wrote outputs/figures/era_evolution.pdf")
    except ImportError:
        print("matplotlib not installed; skipping PDF (install with `pip install -e .[figures]`).")


if __name__ == "__main__":
    main()
