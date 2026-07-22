# IAA analysis pipeline

**Status:** implemented end-to-end; **annotator-2 labels not yet available** — no agreement statistics have been computed or fabricated.

Companion protocol (subset + annotation instructions): [`IAA_PROTOCOL.md`](IAA_PROTOCOL.md).

---

## 1. One command

When annotator-2 segment CSVs are complete for all 20 subset videos:

```bash
cd snatch-phase-bench
source .venv/bin/activate
python scripts/run_iaa_pipeline.py
```

That single command:

1. Loads annotator-1 and annotator-2 segment tables  
2. Aligns videos to the frozen subset manifest  
3. Aligns ontology phase boundaries per video  
4. Computes per-boundary absolute and signed differences  
5. Computes global agreement, per-transition agreement, ICC(2,1), and descriptive statistics  
6. Writes publication-quality **tables** and **figures** under `analysis/iaa/`

### Readiness check (no statistics)

```bash
python scripts/run_iaa_pipeline.py --status
```

Exits `0` only when the pipeline is ready. Prints JSON coverage counts. Does **not** invent agreement numbers.

Current expected behaviour (annotator-2 pending):

```bash
python scripts/run_iaa_pipeline.py
# -> exit code 3, writes analysis/iaa/results/pipeline_status.json only
```

---

## 2. Inputs

| Role | Default path |
|------|----------------|
| Subset manifest | `analysis/iaa/subset_manifest.json` |
| Annotator 1 (primary expert) | `~/papers/Paper_TFM-main/data/annotations/master_segment_labels.csv` |
| Annotator 2 | `analysis/iaa/annotator2/segments/**/*.csv` or `.../master_segment_labels_annotator2.csv` |
| Ontology | `configs/ontology/seven_phase_v1.yaml` |
| FPS | **25** (verified CFR; 1 frame = 40 ms) |

Overrides:

```bash
python scripts/run_iaa_pipeline.py \
  --annotator1 /path/to/a1.csv \
  --annotator2-dir /path/to/a2_segments \
  --fps 25
```

`--allow-partial` runs on the intersection of videos only. **Not permitted for manuscript tables** without explicit disclosure.

---

## 3. Processing stages

```text
manifest (20 videos)
        │
        ├─ load annotator1 CSV ── filter to subset
        ├─ load annotator2 CSVs ─ filter to subset
        │
        ▼
   video alignment (exact video_relpath match)
        │
        ▼
   segments → inclusive frame labels → ontology boundaries
        │
        ▼
   monotonic per-transition matching (A1 ↔ A2)
        │
        ├─ paired rows: frames, signed Δ, |Δ|, ms
        ├─ global descriptive stats + ICC(2,1)
        ├─ per-transition stats + ICC(2,1)
        └─ per-video descriptive stats
        │
        ▼
   tables/  +  figures/  +  results/
```

### 3.1 Video alignment

Videos are the keys in `subset_manifest.json`. Both annotators must provide segments for the same `video_relpath` strings (character-exact, including known spelling variants such as `-88k` / `friedich`).

### 3.2 Boundary alignment

For each video:

1. Convert inclusive segment intervals to a dense phase label vector.  
2. Extract ontology transitions (`setup→first_pull`, …, `catch→recovery`).  
3. Match boundaries **within each transition type** with monotonic one-to-one matching (`match_boundaries_monotonic`).  
4. Record unmatched boundaries as coverage mismatches (common on failed lifts).

### 3.3 Metrics (computed only when data exist)

| Metric | Scope |
|--------|--------|
| Mean / median / P95 / SD / max absolute difference | Global, per-transition, per-video |
| Signed difference (A2 − A1) | Paired rows + Bland–Altman figure |
| ICC(2,1) absolute agreement | Global and per-transition |
| Coverage mismatch counts | Per-transition (only A1 / only A2) |

Implementation: `src/snatch_phase_bench/evaluation/iaa.py`  
Orchestration + I/O: `src/snatch_phase_bench/evaluation/iaa_pipeline.py`  
CLI: `scripts/run_iaa_pipeline.py`

---

## 4. Outputs (created on a successful run)

### 4.1 Results

| Path | Content |
|------|---------|
| `analysis/iaa/results/iaa_agreement.json` | Full numeric payload |
| `analysis/iaa/results/paired_boundaries.csv` | One row per matched boundary |
| `analysis/iaa/results/IAA_RESULTS.md` | Human-readable summary |
| `analysis/iaa/results/pipeline_run_manifest.json` | Artifact index for the run |
| `analysis/iaa/results/pipeline_status.json` | Written on **not-ready** runs only |

### 4.2 Publication tables

| Path | Content |
|------|---------|
| `analysis/iaa/tables/iaa_global.{md,tex}` | Global mean/median/P95 + ICC |
| `analysis/iaa/tables/iaa_per_transition.{md,tex,csv}` | Per-transition agreement |
| `analysis/iaa/tables/iaa_per_video.{md,tex,csv}` | Per-video descriptive stats |

LaTeX tables use `booktabs`-style `\toprule`/`\midrule`/`\bottomrule` and are intended for direct `\input{}` into the manuscript after a successful run.

### 4.3 Publication figures

| Stem (`.png` + `.pdf`) | Content |
|------------------------|---------|
| `iaa_abs_diff_histogram` | Pooled \|Δ\| distribution with mean/median/P95 |
| `iaa_per_transition_boxplot` | \|Δ\| by transition |
| `iaa_per_transition_forest` | Mean \|Δ\| with whisker to P95 |
| `iaa_bland_altman` | Mean frame vs signed Δ (A2−A1) |
| `iaa_coverage_mismatch` | Unmatched boundary counts |
| `iaa_per_video_mean_abs` | Per-video mean \|Δ\| bars |

Directory: `analysis/iaa/figures/`.

Until annotator-2 arrives, these directories contain **READMEs only** — no placeholder numeric plots.

---

## 5. Anti-fabrication policy

1. The pipeline **never** samples fake annotator-2 labels.  
2. Incomplete coverage → non-zero exit; status JSON only.  
3. Unit tests use **synthetic** segment pairs under `tests/`; they do not write study results into `analysis/iaa/results/`.  
4. Manuscript text must not cite agreement numbers until `IAA_RESULTS.md` exists from a complete run.

---

## 6. Annotator-2 deposit checklist

1. Follow [`IAA_PROTOCOL.md`](IAA_PROTOCOL.md) (independence rules).  
2. Optionally build blank templates: `python scripts/prepare_iaa_workpack.py`  
3. Write CSVs to `analysis/iaa/annotator2/segments/<athlete>/<clip>.csv`  
4. `python scripts/run_iaa_pipeline.py --status` → `"ready": true`  
5. `python scripts/run_iaa_pipeline.py`  
6. Copy `tables/*.tex` and `figures/*.pdf` into the paper build as needed  

---

## 7. Tests

```bash
python -m pytest tests/test_iaa.py tests/test_iaa_pipeline.py -q
```

Synthetic only: ICC identities, alignment, table/figure writers on toy data, status refusal path.

---

## 8. Relation to protocol doc

| Document | Role |
|----------|------|
| `IAA_PROTOCOL.md` | What to annotate, which 20 videos, metric rationale (incl. why not κ) |
| `IAA_PIPELINE.md` (this file) | How to compute everything automatically once labels exist |

---

*End of IAA pipeline documentation.*
