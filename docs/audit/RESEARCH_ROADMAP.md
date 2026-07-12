# SnatchPhaseBench — Research Roadmap

**Project vision:** Reframe the MSc thesis work as **SnatchPhaseBench** — a reproducible dataset and benchmark for temporal phase segmentation of the Olympic snatch from markerless pose sequences.

**Guiding principle:** The original LSTM is a **baseline**, not the scientific contribution. The contribution should be the dataset, evaluation protocol, baselines, and audited comparisons.

---

## Priority definitions

| Priority | Meaning |
|----------|---------|
| **P0** | Required before journal submission |
| **P1** | Strongly recommended for scientific credibility |
| **P2** | Optional extensions |

**Effort scale:** low = days; medium = 1–2 weeks; high = multi-week / research-risk.

---

## P0 — Required before paper submission

### P0.1 Exact reproduction of the original experiment

| Field | Detail |
|-------|--------|
| **Objective** | Verify thesis metrics under the original protocol |
| **Technical work** | Resolve LFS binaries; run `verify_project.py --evaluate`; rebuild + compare tensors |
| **Scientific value** | Establishes trust; separates implementation bugs from model claims |
| **Dependencies** | Student repo artifacts, Python 3.12 env |
| **Effort** | **Low** (once binaries available) |

### P0.2 Split and overlap audit

| Field | Detail |
|-------|--------|
| **Objective** | Determine precisely whether metrics are inflated by stride-1 window overlap |
| **Technical work** | Tests for athlete/video/frame leakage; quantify overlap; window vs frame vs segment evaluation |
| **Scientific value** | Core methodological contribution; avoids misinterpretation of high accuracy |
| **Dependencies** | P0.1 or rebuilt dataset |
| **Effort** | **Medium** |

### P0.3 Segment-level metrics

| Field | Detail |
|-------|--------|
| **Objective** | Evaluate temporal segmentation quality, not only window classification |
| **Technical work** | Implement frame aggregation, segment extraction, edit score, F1@10/25/50, boundary metrics |
| **Scientific value** | Aligns evaluation with task definition (phase segmentation) |
| **Dependencies** | Ground-truth segment labels (`master_segment_labels.csv`) |
| **Effort** | **Medium** |

### P0.4 Athlete-level cross-validation

| Field | Detail |
|-------|--------|
| **Objective** | Report mean ± std over multiple athlete folds, not a single split |
| **Technical work** | K-fold or repeated holdout by athlete; fixed seed protocol |
| **Scientific value** | Generalization estimate with uncertainty |
| **Dependencies** | P0.2 split audit |
| **Effort** | **Medium** |

### P0.5 Trivial baselines

| Field | Detail |
|-------|--------|
| **Objective** | Anchor learned models against sane lower bounds |
| **Technical work** | Majority class; persistence (predict previous phase); phase-frequency prior |
| **Scientific value** | Demonstrates problem difficulty and class imbalance effects |
| **Dependencies** | Dataset loader |
| **Effort** | **Low** |

### P0.6 GRU baseline

| Field | Detail |
|-------|--------|
| **Objective** | Compare LSTM to closely related recurrent baseline |
| **Technical work** | GRU with matched capacity and training protocol |
| **Scientific value** | Standard ablation expected by reviewers |
| **Dependencies** | Training pipeline |
| **Effort** | **Low** |

### P0.7 Temporal Convolutional Network (TCN)

| Field | Detail |
|-------|--------|
| **Objective** | Strong classical temporal baseline for action segmentation |
| **Technical work** | Single- or multi-stage dilated TCN on pose sequences |
| **Scientific value** | Common benchmark in temporal action segmentation literature |
| **Dependencies** | Frame/sequence dataloader |
| **Effort** | **Medium** |

### P0.8 MS-TCN / MS-TCN++

| Field | Detail |
|-------|--------|
| **Objective** | Canonical multi-stage segmentation architecture |
| **Technical work** | Adapt MS-TCN++ to 99-d pose input; same splits/metrics |
| **Scientific value** | Strong, widely recognized segmentation baseline |
| **Dependencies** | P0.3 segment metrics |
| **Effort** | **High** |

### P0.9 ST-GCN (or equivalent skeleton graph model)

| Field | Detail |
|-------|--------|
| **Objective** | Exploit skeletal graph structure instead of flat 99-d vectors |
| **Technical work** | MediaPipe topology → graph; ST-GCN or CTR-GCN-lite |
| **Scientific value** | Tests whether graph inductive bias helps phase boundaries |
| **Dependencies** | Normalized coordinates; graph definition |
| **Effort** | **High** |

### P0.10 Lightweight Transformer temporal model

| Field | Detail |
|-------|--------|
| **Objective** | Modern sequence baseline with controlled capacity |
| **Technical work** | Temporal Transformer / Performer-lite on windowed or full sequences |
| **Scientific value** | Reviewers expect Transformer comparison in 2026 segmentation papers |
| **Dependencies** | Training stability tuning |
| **Effort** | **High** |

### P0.11 Statistical comparison

| Field | Detail |
|-------|--------|
| **Objective** | Compare models beyond point estimates |
| **Technical work** | Bootstrap CIs over athletes/videos; paired tests across folds |
| **Scientific value** | Supports claims like "model A significantly improves F1@25" |
| **Dependencies** | P0.4 cross-validation |
| **Effort** | **Medium** |

---

## Proposed baseline implementation order

This order minimizes rework and validates infrastructure early:

1. **P0.1** Exact reproduction / rebuild path  
2. **P0.2** Split + overlap audit (parallel with metric tooling design)  
3. **P0.3** Segment-level metrics module  
4. **P0.5** Trivial baselines  
5. **P0.6** LSTM (ported) + GRU  
6. **P0.7** TCN  
7. **P0.8** MS-TCN++  
8. **P0.9** ST-GCN  
9. **P0.10** Lightweight Transformer  
10. **P0.4** Athlete CV + **P0.11** statistical comparison  

---

## P1 — Strongly recommended

### P1.1 Coordinate normalization

| Field | Detail |
|-------|--------|
| **Objective** | Reduce camera/anthropometry sensitivity |
| **Technical work** | Hip-center origin; shoulder/hip scale; facing normalization |
| **Scientific value** | Likely improves cross-athlete generalization |
| **Dependencies** | Preprocessing module |
| **Effort** | **Medium** |

### P1.2 x,y versus x,y,z ablation

| Field | Detail |
|-------|--------|
| **Objective** | Quantify value of depth coordinates from monocular pose |
| **Technical work** | Toggle z in dataset builder; matched models |
| **Scientific value** | Informs input representation for benchmark spec |
| **Dependencies** | Config-driven preprocessing |
| **Effort** | **Low** |

### P1.3 Window-size and stride ablations

| Field | Detail |
|-------|--------|
| **Objective** | Measure sensitivity to overlap and temporal context |
| **Technical work** | Windows {15,31,61}, strides {1,5,15} |
| **Scientific value** | Directly addresses overlapping-window concern |
| **Dependencies** | P0.2 overlap audit |
| **Effort** | **Medium** |

### P1.4 Landmark-noise robustness

| Field | Detail |
|-------|--------|
| **Objective** | Simulate pose estimator jitter |
| **Technical work** | Gaussian noise / dropout on landmarks at train or test time |
| **Scientific value** | Practical robustness for markerless pipelines |
| **Dependencies** | Augmentation pipeline |
| **Effort** | **Medium** |

### P1.5 Missing-landmark robustness

| Field | Detail |
|-------|--------|
| **Objective** | Handle occluded/low-confidence joints |
| **Technical work** | Random landmark masking; compare interpolation vs learned masking |
| **Scientific value** | Real-world deployment relevance |
| **Dependencies** | Visibility columns available in keypoint CSVs |
| **Effort** | **Medium** |

### P1.6 Frame-rate sensitivity

| Field | Detail |
|-------|--------|
| **Objective** | Test temporal subsampling effects |
| **Technical work** | Downsample pose sequences; re-map segment boundaries |
| **Scientific value** | Assesses portability across capture setups |
| **Dependencies** | Known native FPS per clip (may need student input) |
| **Effort** | **Medium** |

### P1.7 Inter-annotator agreement plan

| Field | Detail |
|-------|--------|
| **Objective** | Quantify annotation noise ceiling |
| **Technical work** | Re-annotate subset; compute Cohen's kappa / frame IoU |
| **Scientific value** | Contextualizes model performance vs human disagreement |
| **Dependencies** | Second annotator + time |
| **Effort** | **High** |

### P1.8 Clear biomechanical phase definitions

| Field | Detail |
|-------|--------|
| **Objective** | Document operational definitions used for labels |
| **Technical work** | Phase boundary criteria, figures, edge-case rules |
| **Scientific value** | Essential for dataset paper and external reuse |
| **Dependencies** | Student/supervisor biomechanics input |
| **Effort** | **Medium** |

---

## P2 — Optional extensions

### P2.1 Learning curves

| Field | Detail |
|-------|--------|
| **Objective** | Data efficiency analysis |
| **Technical work** | Train on increasing fractions of athletes |
| **Scientific value** | Guides dataset expansion priorities |
| **Dependencies** | P0.4 CV |
| **Effort** | **Medium** |

### P2.2 Subgroup analysis

| Field | Detail |
|-------|--------|
| **Objective** | Performance by sex, weight class, success/fail attempts |
| **Technical work** | Parse metadata from filenames; stratified metrics |
| **Scientific value** | Fairness and biomechanics insights |
| **Dependencies** | Reliable metadata parsing |
| **Effort** | **Low–medium** |

### P2.3 Camera-angle analysis

| Field | Detail |
|-------|--------|
| **Objective** | Assess viewpoint sensitivity |
| **Technical work** | Tag angles; per-angle metrics if metadata exists |
| **Scientific value** | Deployment guidance |
| **Dependencies** | Video metadata (likely missing) |
| **Effort** | **High** |

### P2.4 Model efficiency

| Field | Detail |
|-------|--------|
| **Objective** | Latency, parameters, FLOPs |
| **Technical work** | Profiling on CPU/GPU |
| **Scientific value** | Practical benchmarking dimension |
| **Dependencies** | Trained models |
| **Effort** | **Low** |

### P2.5 Real-time inference

| Field | Detail |
|-------|--------|
| **Objective** | Streaming phase prediction |
| **Technical work** | Causal models + smoothing; demo pipeline |
| **Scientific value** | Applied coaching scenario |
| **Dependencies** | P2.4 |
| **Effort** | **High** |

### P2.6 Extension to clean and jerk

| Field | Detail |
|-------|--------|
| **Objective** | Broaden benchmark to second lift |
| **Technical work** | New annotations, phases, splits |
| **Scientific value** | Larger impact; new dataset collection |
| **Dependencies** | New data + legal clearance |
| **Effort** | **High** |

---

## Paper packaging milestones

| Milestone | Deliverables |
|-----------|--------------|
| M1 — Audit complete | `PROJECT_AUDIT.md`, reproduction plan (this phase) |
| M2 — Reproduction verified | Exact or functional reproduction documented |
| M3 — Benchmark MVP | Segment metrics + trivial/LSTM/GRU/TCN baselines |
| M4 — Full benchmark | MS-TCN, ST-GCN, Transformer + CV + stats |
| M5 — Public artifact | Zenodo release with docs, configs, splits, keypoints (if licensed) |

---

## Risk register (summary)

| Risk | Mitigation |
|------|------------|
| Video/license blockage for public release | Publish pose + annotations only with permission; keep videos private |
| Overlap-inflated legacy metrics | Reframe paper around corrected evaluation |
| Single-split optimism | Athlete CV in P0.4 |
| Annotation subjectivity | P1.7 agreement study or explicit limitation |
