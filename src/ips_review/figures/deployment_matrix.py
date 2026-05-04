"""Figure: deployment-readiness matrix (Section VI)."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    src = Path("data/processed/section_mapping.csv")
    if not src.exists():
        raise SystemExit(f"Run the pipeline first; missing {src}")
    df = pd.read_csv(src, comment="#", encoding="utf-8-sig")
    cols = [c for c in df.columns if c.startswith("Sec_VI_Deploy_")]
    sense = [c for c in df.columns if c.startswith("Sec_IV_Sensing_")]

    bool_df = df[cols + sense].apply(lambda s: s.astype(str).isin(["True", "1", "true"]))
    matrix = pd.DataFrame(
        index=[c.replace("Sec_IV_Sensing_", "") for c in sense],
        columns=[c.replace("Sec_VI_Deploy_", "") for c in cols],
        dtype=int,
    )
    for s_col in sense:
        for d_col in cols:
            matrix.at[s_col.replace("Sec_IV_Sensing_", ""), d_col.replace("Sec_VI_Deploy_", "")] = int(
                (bool_df[s_col] & bool_df[d_col]).sum()
            )

    out_dir = Path("outputs/tables"); out_dir.mkdir(parents=True, exist_ok=True)
    matrix.to_csv(out_dir / "deployment_matrix.csv")
    print(matrix)
    print("Wrote outputs/tables/deployment_matrix.csv")


if __name__ == "__main__":
    main()
