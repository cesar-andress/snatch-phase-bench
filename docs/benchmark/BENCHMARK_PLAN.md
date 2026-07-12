# Benchmark plan

**Status:** Planning document (Phase 3+). Frozen LSTM baseline is not part of this benchmark tier system except as a historical reproduction artifact.

**Scientific guidance:** [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md) Parts 3, 4, 6, and 12.

**Gap analysis:** [`../literature/GAP_ANALYSIS.md`](../literature/GAP_ANALYSIS.md)

---

## 1. Benchmark philosophy

SnatchPhaseBench is a **reproducible benchmark**, not a single-model paper.

### 1.1 Honest positioning

The defensible contributions (ranked):

1. **Dataset** — annotated snatch attempts with athlete-disjoint evaluation
2. **Benchmark protocol** — fixed preprocessing, splits, metrics, and baselines
3. **Domain formalization** — short-horizon TAS with biomechanically meaningful boundaries
4. **Software** — supporting artifact
5. **New architecture** — **not claimed**

Core scientific question:

> Where do learned temporal segmenters improve over the knee-angle heuristic the biomechanics community already uses—and where do they not?

A result where learning ties the rule-based baseline on clean sagittal video is **publishable** if reported honestly with boundary-level analysis.

### 1.2 Three-stage pipeline (do not blur roles)

All models must respect this separation (literature Part 4.2):

```text
[Stage 1] Pose estimation     →  fixed keypoints (MediaPipe v1 benchmark)
[Stage 2] Skeleton encoding   →  optional (raw / CTR-GCN / PoseC3D)
[Stage 3] Temporal segmentation → per-frame phase labels
```

- **ST-GCN, CTR-GCN** = encoders (recognition backbones), not segmenters
- **MS-TCN, ASFormer** = segmenters
- **MotionBERT, PoseFormer** = pose representations / 3D lifting — upstream, not segmentation baselines

### 1.3 Fair-comparison protocol

- Single codebase, single preprocessing, single split file shipped with dataset
- Identical metric implementation (`snatch_phase_bench.evaluation`)
- Fixed random seeds; report mean ± SD over seeds and/or folds
- Fixed training budget and hyperparameter search protocol per model family
- Release code, splits, eval script, and environment spec

---

## 2. Baseline hierarchy

### Tier 0 — Essential (non-negotiable)

| ID | Model | Role | Repo status |
|----|-------|------|-------------|
| **B0** | Rule-based knee-angle threshold segmenter | Biomechanics heuristic; **primary competitor** | **Not implemented** |
| **B1** | Raw normalized keypoints → MS-TCN | Standard TAS baseline | Not implemented |
| **B2** | MS-TCN++ | Refined TAS baseline | Not implemented |
| **B3** | ASFormer | Strong attention baseline | Not implemented |

**Historical note:** The frozen **LSTM window classifier** (thesis) remains in `training/lstm_trainer.py` for reproduction only. It is **not** the literature-recommended benchmark baseline. Report it separately as “thesis replication baseline” if needed.

### Tier 1 — Recommended

| ID | Model | Role | Repo status |
|----|-------|------|-------------|
| **A1** | DiffAct | Advanced generative TAS | Not implemented |
| **A2** | CTR-GCN encoder → MS-TCN/ASFormer head | Skeleton encoder contribution | Not implemented |
| **A3** | PoseC3D heatmap → segmentation head | Representation contrast | Not implemented |

### Tier 2 — Optional reach

| ID | Model | When to include |
|----|-------|-----------------|
| A4 | ActFusion | Only if Tier 0–1 complete and venue expects SOTA reach |
| — | OnlineTAS | Only if claiming real-time / streaming |
| — | HD-GCN, InfoGCN | **Excessive** for 5–7 phases; cite as context, do not run all |

### Trivial baselines (anchor learned models)

- Majority class
- Persistence (predict previous phase)
- Phase-frequency prior

---

## 3. Future models and registration

Implement via `models/registry.py` without modifying frozen baseline modules.

| Model | Registry name (planned) | Output type | Priority |
|-------|-------------------------|-------------|----------|
| Rule-based knee-angle | `rule_knee_angle` | Per-frame | P0 |
| MS-TCN | `ms_tcn` | Per-frame | P0 |
| MS-TCN++ | `ms_tcn_pp` | Per-frame | P0 |
| ASFormer | `asformer` | Per-frame | P0 |
| DiffAct | `diffact` | Per-frame | P1 |
| CTR-GCN + TAS head | `ctr_gcn_ms_tcn` | Per-frame | P1 |
| PoseC3D + TAS head | `posec3d_ms_tcn` | Per-frame | P1 |
| GRU (matched to LSTM) | `gru_baseline` | Window or frame | P2 — ablation only |
| LSTM (thesis) | `lstm_baseline` | Window | Frozen reproduction only |

**Gate:** Do not register Tier 0 learned models until `best_model.pt` checkpoint validation passes (`docs/FROZEN_BASELINE.md`).

---

## 4. Evaluation metrics

Primary metrics (literature Part 3.3, 6.4):

| Metric | Purpose | Implementation |
|--------|---------|----------------|
| Frame accuracy (MoF) | Comparability with TAS literature | `frame.py` |
| Segmental edit score | Penalize over-segmentation | `segment.py` |
| Segmental F1@10/25/50 | Boundary-aware segment matching | `segment.py` |
| **Boundary MAE (ms)** | **Primary differentiator** — per transition | `boundary.py` TODO |
| **Boundary within-τ (%)** | % boundaries within ±1,2,3 frames | `boundary.py` TODO |
| Per-phase recall | Expose short-phase collapse | Extend `window.py` / reports |
| Per-transition breakdown | Highlight Second Pull→Turnover | **Not implemented** |

Secondary (thesis compatibility only):

| Metric | Note |
|--------|------|
| Window-level accuracy / macro-F1 | Frozen LSTM protocol; susceptible to saturation |

Report **segment + boundary metrics first** in all benchmark tables; window metrics in appendix or secondary column.

See [`../evaluation_metrics.md`](../evaluation_metrics.md) for mathematical definitions.

---

## 5. Evaluation protocol

### 5.1 Splits

| Protocol | Current | Target |
|----------|---------|--------|
| Athlete-disjoint holdout | 49/10/11 fixed split ✓ | Keep as primary reported split |
| Grouped leave-one-athlete-out | Not implemented | **Required** for uncertainty (literature Part 3.5) |
| Random clip split | **Forbidden** | Never — leakage kill-shot |

### 5.2 Input standardization (fixed across all models)

- Pose extractor: MediaPipe Pose Landmarker (33 landmarks, x/y/z) for benchmark v1
- Root-centered, scale-normalized coordinates (document exact formula)
- Native FPS preserved; document downsampling ablation separately
- Identical train-only standardization policy

### 5.3 Training recipe

- Early stopping on validation macro-F1 (or segment-F1@50 for dense models)
- Class weighting where appropriate
- Document epochs, batch size, learning rate search budget per model
- Control training recipe — ST-GCN++ “good practices” lesson: recipe dominates architecture

---

## 6. Robustness studies

| Experiment | Purpose | Priority |
|------------|---------|----------|
| Pose-extractor swap (HRNet vs MediaPipe vs RTMPose) | Quantify extractor dependence | P1 |
| Camera angle (frontal / sagittal / oblique) | Domain shift | P1 |
| Occlusion / plate blocking | Catch-phase failures | P1 |
| Motion blur at second pull | Fast segment boundaries | P2 |
| Frame-rate downsampling | Deployment realism | P2 |
| Athlete morphology / weight class | Generalization | P1 |

---

## 7. Ablation studies

| Factor | Variants | Question |
|--------|----------|----------|
| Input representation | Raw keypoints vs CTR-GCN vs PoseC3D | Do heavy encoders help on short 5–7 phase motion? |
| Dimensionality | 2D vs 3D lifted pose | Worth MotionBERT/OpenCap path? |
| Multi-stage refinement | MS-TCN stages on/off | Does refinement help at ~2–6 s horizon? |
| Smoothing loss weight | MS-TCN truncated MSE | Over-segmentation sensitivity |
| Window vs dense | LSTM windows vs MS-TCN frames | Thesis vs TAS framing |
| Visibility features | With/without MediaPipe visibility | Cheap feature ablation |

---

## 8. Runtime analysis

Report for each model on specified CPU and GPU:

- Parameter count
- FLOPs (optional)
- End-to-end FPS (pose + encode + segment)
- Training wall-clock time

Populate `~/papers/snatch-phase-bench/paper/sections/06_results.tex` `tab:runtime` when hardware is standardized.

---

## 9. Publication milestones

Aligned with literature Part 12 prioritized roadmap:

| Milestone | Deliverable | Blocks |
|-----------|-------------|--------|
| **M0** | Checkpoint validation (`best_model.pt`) | All benchmark training |
| **M1** | Phase ontology reconciliation (5 vs 7) | Methods + dataset text |
| **M2** | B0 rule-based baseline + boundary metrics | Core scientific credibility |
| **M3** | B1–B3 TAS baselines under frozen recipe | Main results table |
| **M4** | LOAO or grouped k-fold results | Uncertainty reporting |
| **M5** | Pose-extractor + camera robustness | Reviewer risk mitigation |
| **M6** | A1–A3 advanced contrasts | Optional enrichment |
| **M7** | Public release (data route + Zenodo) | Submission |
| **M8** | Manuscript results population | Submission |

Target venues (see [`../release/PUBLICATION_STRATEGY.md`](../release/PUBLICATION_STRATEGY.md)): **Sensors**, **Biomedical Signal Processing and Control**.

---

## 10. Software integration checklist

When implementing each benchmark model:

- [ ] Register in `models/registry.py`
- [ ] Add YAML config under `configs/benchmark/`
- [ ] Extend `experiments/runner.py` (post-gate)
- [ ] Add tests for output shape and determinism
- [ ] Log results to `outputs/benchmark/<model>/`
- [ ] Update `docs/paper/PAPER_TODO.md` and external `~/papers/snatch-phase-bench/paper/WRITING_STATUS.md`
- [ ] Populate manuscript tables only after verified run

---

## 11. Related documents

- [`../research_design.md`](../research_design.md) — scientific goals
- [`../evaluation_metrics.md`](../evaluation_metrics.md) — metric math
- [`../paper/REVIEWER_CHECKLIST.md`](../paper/REVIEWER_CHECKLIST.md) — risk mitigation
- [`../SCIENTIFIC_WORKFLOW.md`](../SCIENTIFIC_WORKFLOW.md) — sync process
- [`../paper/MANUSCRIPT_LOCATION.md`](../paper/MANUSCRIPT_LOCATION.md) — external LaTeX path
