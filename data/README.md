# Data directory policy

**Phase 1:** This directory is intentionally empty except for placeholders.

## Intended layout

| Subdirectory | Purpose |
|--------------|---------|
| `raw/` | Original videos (typically **not** redistributable) |
| `interim/` | Extracted keypoints, intermediate CSVs |
| `processed/` | Windowed tensors, split indices, label maps |

## Rules

1. Do **not** copy raw competition videos here without confirmed redistribution rights.
2. Do **not** commit large generated files; use `.gitignore` and Zenodo for releases.
3. **Copy** needed files from `~/papers/Paper_TFM-main` into `data/interim/` or `data/processed/` here. Never modify the snapshot.
4. Remove or pseudonymize athlete-identifying paths before any public release.

## Source material (read-only snapshot)

Read from (never write to):

`~/papers/Paper_TFM-main/data/`

Copy into this repository:

| Source (read-only) | Destination (canonical) |
|--------------------|-------------------------|
| `data/keypoints/` | `data/interim/keypoints/` |
| `data/annotations/master_*.csv` | `data/interim/` |
| `outputs/lstm_phases/athlete_split.json` | `data/processed/` |
| Real LFS binaries (from student) | `data/processed/`, `outputs/baseline/` |

See [`../docs/audit/PROJECT_AUDIT.md`](../docs/audit/PROJECT_AUDIT.md) for availability status.
