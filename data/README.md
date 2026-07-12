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
3. Prefer **symlinks or documented paths** to the read-only student repository during reproduction.
4. Remove or pseudonymize athlete-identifying paths before any public release.

## Source material (read-only)

Original thesis artifact path (local audit machine):

`/home/cesar/papers/Paper_TFM-main/data/`

Key files expected for reproduction:

- `annotations/master_frame_labels.csv`
- `annotations/master_segment_labels.csv`
- `keypoints/**/*.csv`
- `processed/meta.csv` (metadata; tensors may require Git LFS fetch)

See [`../../PROJECT_AUDIT.md`](../../PROJECT_AUDIT.md) for availability status.
