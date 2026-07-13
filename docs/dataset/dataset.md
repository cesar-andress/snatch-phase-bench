# SnatchPhaseBench Dataset Documentation

## Overview

The dataset comprises **208 snatch attempts** from **70 athletes**, annotated into **seven biomechanical phases** plus an `unlabeled` class used during annotation but excluded from training windows.

**Status:** Structure verified during Phase 2 reproduction. Author clarifications integrated 2026-07-13 ([`reproduction/AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md)). Public release pending legal review.

---

## Directory structure (read-only snapshot)

```text
Paper_TFM-main/data/
  annotations/
    master_frame_labels.csv      # canonical frame labels
    master_segment_labels.csv    # segment intervals
    frame_labels/<athlete>/*.csv
    segment_labels/<athlete>/*.csv
  keypoints/<athlete>/*.csv      # MediaPipe Pose Landmarker output
  processed/                     # frozen tensors (LFS in snapshot export)
```

Canonical rebuilt copy (gitignored):

```text
data/processed/rebuilt/
  X.npy, y.npy, meta.csv, label_map.csv
```

---

## Annotations

### Frame labels (`master_frame_labels.csv`)

| Column | Description |
|--------|-------------|
| `video_relpath` | Relative path, e.g. `athlete/clip.mp4` |
| `frame` | Frame index |
| `phase_id` | Integer class ID |
| `phase_name` | Human-readable phase |

**Verified:** 35,825 frame rows (canonical corrected `master_frame_labels.csv`); 208 videos; no duplicate (video, frame) conflicts. An earlier 37,125-row export contained duplicates and filename errors (see [`AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md)).

### Segment labels (`master_segment_labels.csv`)

Contiguous intervals per phase. **Verified:** 856 per-video segment CSV files present.

### Class definitions

| phase_id | phase_name | In training? |
|----------|------------|--------------|
| 0 | unlabeled | No (dropped at window center) |
| 1 | setup | Yes |
| 2 | first_pull | Yes |
| 3 | transition | Yes |
| 4 | second_pull | Yes |
| 5 | turnover | Yes |
| 6 | catch | Yes |
| 7 | recovery | Yes |

**Phase ontology (documented):** Coaching literature uses three--four pulling phases; computer-vision work commonly uses six phases from barbell and joint-angle events (Cao et al., 2022; Chen et al., 2022). This dataset adds **Setup** to that six-phase CV model, yielding **seven** supervised labels with separate `turnover` and `catch`. Full rationale: [`reproduction/AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md). Mapping to the five-phase knee-angle standard (Thiele et al., 2024) informs B0 only.

---

## Splits

Athlete-level split in `outputs/lstm_phases/athlete_split.json` (read-only snapshot):

| Split | Athletes | Videos | Windows |
|-------|----------|--------|---------|
| Train | 49 | 145 | 14,140 |
| Val | 10 | 30 | 3,232 |
| Test | 11 | 33 | 3,877 |

**Verified:** No athlete or video overlap across splits (automated test PASS).

---

## Keypoint format

Each CSV row = one video frame.

- Extracted with **MediaPipe 0.10.30**, **Full** Pose Landmarker model
- 33 MediaPipe landmarks × (x, y, z) = **99 numeric columns**
- Optional visibility columns (`v0`…`v32`) — **not used** by frozen baseline
- Interpolation + forward/backward fill for missing values (frozen preprocessing)

**Verified:** 208 keypoint CSV files.

**Known issue:** Three filenames contain a **space before `.csv`**; matching `video_relpath` entries include the same space — rebuild succeeds.

---

## Preprocessing pipeline (frozen)

1. Merge frame labels with keypoints on `(video_relpath, frame)`.
2. Build sliding windows: size **31**, stride **1**.
3. Label = phase at **center frame**.
4. Drop windows whose center is `unlabeled`.

Output tensor shape: **`(21249, 31, 99)`**.

**Verified:** Rebuilt `X.npy` / `y.npy` SHA-256 matches `baseline_tfm/manifest.json`.

---

## Generated tensors

| File | Shape / rows | dtype |
|------|--------------|-------|
| `X.npy` | (21249, 31, 99) | float32 |
| `y.npy` | (21249,) | int64 |
| `meta.csv` | 21249 rows | CSV |
| `label_map.csv` | 8 phases | CSV |

### Class distribution (windows, verified from rebuild)

| Phase | Windows (approx.) |
|-------|-------------------|
| setup | 6017 |
| first_pull | 2434 |
| transition | 673 |
| second_pull | 1245 |
| turnover | 1903 |
| catch | 1912 |
| recovery | 7065 |

---

## Future work

- [ ] Pseudonymize athlete folder names for public release
- [ ] Document native FPS and camera angles
- [ ] Inter-annotator agreement study
- [ ] Publish segment labels as primary benchmark format
- [ ] Zenodo DOI with legal clearance
