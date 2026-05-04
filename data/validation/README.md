# `data/validation/`

Place stratified validation samples and human-coded outputs here.

## Recommended file naming

| Filename | What it is |
|---|---|
| `sample_v1.0.csv` | Output of `ips-review sample` against dictionary v1.0; carries `Human_Label` empty column |
| `sample_v1.0.blinded.csv` | `Screen_Label` removed and rows shuffled; what reviewers receive |
| `sample_v1.0.coded_by_<reviewer>.csv` | One per reviewer with `Human_Label` filled |
| `sample_v1.0.consensus.csv` | Adjudicated consensus labels across reviewers |

Run `ips-review validate ...` against the consensus file to produce the
report in `outputs/reports/`.

See [`docs/validation_protocol.md`](../../docs/validation_protocol.md)
for the full protocol.
