# Literature gap analysis

**Date:** 2026-07-13  
**External reference (authoritative, read-only):** [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md)

This document compares the literature foundation against the current SnatchPhaseBench repository and identifies what is covered, missing, inconsistent, or obsolete.

---

## 1. Executive summary

The repository has strong **reproducibility infrastructure** and a **verified dataset rebuild**, but the scientific strategy in the literature foundation is **ahead of the codebase** in three critical areas:

1. **Baseline hierarchy** — literature mandates a rule-based knee-angle baseline (B0) and TAS models (MS-TCN, ASFormer); repo only has a frozen window-level LSTM.
2. **Evaluation emphasis** — literature prioritizes boundary timing in milliseconds and segment-level F1; repo implements segment metrics in software but baseline protocol remains window-level only.
3. **Contribution framing** — literature rejects “novel LSTM” framing; some legacy docs still list GRU/LSTM comparisons as primary benchmark goals.

The largest **ontology documentation gap** is **closed** as of 2026-07-13: author clarifications in [`reproduction/AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md) document the seven-class taxonomy and its relation to six-phase CV literature and the five-phase knee-angle standard. **B0 mapping** to five phases remains implementation work.

---

## 2. Topic-by-topic comparison

### 2.1 Research map (seven scientific areas)

| Topic (literature Part 1) | Repository coverage | Gap |
|---------------------------|---------------------|-----|
| Pose estimation | `docs/dataset/dataset.md` (MediaPipe); audit notes LFS task file | No extractor comparison ablation; no pose-error quantification |
| Markerless validity | Not documented in repo | **Missing** — need Theia3D/OpenCap validity framing in `research_design.md` |
| Skeleton action recognition | `models/registry.py` stub; paper Related Work outline | No ST-GCN/CTR-GCN encoders; distinction encoder vs segmenter not in architecture doc until now |
| Temporal action segmentation | `evaluation/metrics/segment.py`; `evaluation_metrics.md` | MS-TCN/ASFormer not implemented; LSTM is not standard TAS baseline |
| Sports analytics / biomechanics | Paper introduction draft | No dedicated sports-CV prior-art table in repo |
| Weightlifting analysis | `dataset/dataset.md`, audit | Phase ontology not tied to biomechanics citations |
| Reproducibility culture | `reproduction/`, `FROZEN_BASELINE.md`, `SCIENTIFIC_WORKFLOW.md` (new) | Zenodo/public release pending |

### 2.2 Benchmark recommendations (literature Part 6)

| Literature recommendation | Repository status | Gap |
|---------------------------|-------------------|-----|
| **B0 rule-based knee-angle segmenter** | Not implemented | **Critical missing baseline** |
| **B1–B3** MS-TCN, MS-TCN++, ASFormer | Not implemented | Planned in old roadmap as “Phase 3” |
| **A1** DiffAct | Not implemented | Optional advanced |
| **A2/A3** CTR-GCN / PoseC3D encoders → TAS head | Not implemented | Architecture pattern not coded |
| Grouped leave-one-athlete-out CV | Single fixed split (49/10/11) | Split validated but no k-fold LOAO |
| Frozen training recipe across models | `baseline_lstm.yaml` only | No multi-model recipe |
| Boundary metrics (ms per transition) | `boundary.py` TODO | **Not implemented** |
| Pose-extractor robustness ablation | Not planned in code | Documented in benchmark plan only |
| Runtime / FLOPs / FPS reporting | Not implemented | Table shell in paper only |

### 2.3 Evaluation recommendations (literature Part 3.3–3.6)

| Metric (literature) | Repo module | Baseline uses? | Gap |
|---------------------|-------------|----------------|-----|
| Frame accuracy / MoF | `frame.py` | No | Need dense per-frame predictions from TAS models |
| Segmental edit score | `segment.py` | No | Implemented, not reported |
| Segmental F1@10/25/50 | `segment.py` | No | Implemented, not reported |
| Boundary MAE (frames/ms) | `boundary.py` | No | **TODO in code** |
| Boundary F1 ± tolerance | `boundary.py` | No | **TODO in code** |
| Per-transition breakdown | Not implemented | No | **Missing** — literature says Second Pull→Turnover is key |
| Window-level accuracy | `window.py` | **Yes (frozen)** | Literature warns metric saturation — correctly flagged in limitations |

### 2.4 Literature organization (literature Part 8)

| Manuscript section blueprint | `~/papers/snatch-phase-bench/paper/sections/` (external) | Repo doc |
|---------------------------------|--------------------------------------------------|----------|
| Markerless pose + validity | Outline only, no citations | **Missing** dedicated doc — split across `dataset.md`, `research_design.md` |
| Skeleton action recognition | Outline | `benchmark/BENCHMARK_PLAN.md` (new) |
| Temporal action segmentation | Outline | `evaluation_metrics.md` |
| Sports motion / phase analysis | Outline | `benchmark/BENCHMARK_PLAN.md` |
| Weightlifting CV prior art | Outline | `GAP_ANALYSIS.md` §2.5 below |
| Benchmarks & reproducibility | Partial in intro | `reproduction/`, `SCIENTIFIC_WORKFLOW.md` |

### 2.5 Publication strategy (literature Part 7)

| Literature guidance | Repository status | Gap |
|--------------------|-------------------|-----|
| Contribution = dataset + benchmark + formalization | Partially in `research_design.md` | Needs explicit “do not claim method novelty” |
| Target Sensors / BSPC | Not documented | **`release/PUBLICATION_STRATEGY.md`** (new) |
| Avoid Pattern Recognition as primary | Not documented | Added to publication strategy |
| Honest story sentence (benchmark vs heuristic) | Paper abstract draft aligns | Reinforce in `research_design.md` |

### 2.6 Future work (literature Part 11)

| Literature item | In repo? | Notes |
|-----------------|----------|-------|
| Real-time coaching (OnlineTAS) | Paper discussion TODO | Correctly deferred |
| Weak supervision | Not in repo | Future work only |
| Multi-view fusion | Not in repo | Needs capture |
| Clean & jerk extension | Not in repo | Dataset expansion |
| 3D pose (MotionBERT) | Mentioned in old roadmap | Align with literature Tier 2 |

### 2.7 Reviewer risks (literature Part 10)

| Risk | Addressed in repo? | Document |
|------|-------------------|----------|
| “Why not knee-angle rules?” | **No B0 baseline** | `paper/REVIEWER_CHECKLIST.md` |
| No methodological novelty | Partially (paper framing) | `research_design.md` update |
| Dataset too small | Counts verified; demographics missing | `dataset/dataset.md` TODOs |
| Pose unreliable at catch | Limitation stated | Need measurement ablation |
| Data leakage | Split test PASS | Document prominently |
| Extractor dependence | Not tested | Benchmark plan |
| Metric saturation | Limitation stated | Boundary metrics plan |
| Not reproducible | Strong infra | Checkpoint still missing |
| Annotation subjectivity | Stated | No IAA study |
| Overclaimed novelty | Paper cautions | Reviewer checklist |

---

## 3. Documentation already covered (adequate)

| Area | Location | Assessment |
|------|----------|------------|
| Dataset counts, splits, tensors | `docs/dataset/dataset.md` | **Good** — verified numbers |
| Reproduction SHA-256 match | `docs/reproduction/REPRODUCTION_SUMMARY.md` | **Good** — frozen |
| Window overlap / autocorrelation | `docs/reproduction/temporal_autocorrelation.md` | **Good** — supports reviewer risk #7 |
| Metric math (window/frame/segment) | `docs/evaluation_metrics.md` | **Good** — extend for boundary-ms |
| Software architecture | `docs/project_architecture.md` | **Good** — needs 3-stage pipeline note |
| Frozen baseline policy | `docs/FROZEN_BASELINE.md` | **Good** |
| Manuscript structure | External `~/papers/snatch-phase-bench/paper/` + `docs/paper/PAPER_TODO.md` | **Good** |
| Phase 1 audit | `docs/audit/PROJECT_AUDIT.md` | **Good** — historical |

---

## 4. Documentation missing (before submission)

| Missing item | Priority | Target location |
|--------------|----------|-----------------|
| Rule-based kinematic baseline spec | P0 | `docs/benchmark/BENCHMARK_PLAN.md` + future `models/` |
| Phase ontology reconciliation (5 vs 7 phases) | P0 | **Documented** — [`reproduction/AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md); B0 mapping still open |
| Boundary timing metric specification | P0 | `docs/evaluation_metrics.md` |
| Prior-art comparison table (weightlifting CV) | P1 | `docs/literature/PRIOR_ART_WEIGHTLIFTING.md` or paper |
| Verified bibliography workflow | P1 | `docs/paper/PAPER_TODO.md` |
| Inter-annotator agreement protocol | P1 | `docs/dataset/ANNOTATION_PROTOCOL.md` (future) |
| LOAO / grouped k-fold split generator | P1 | `src/` + `docs/benchmark/` |
| Pose error validation subset | P2 | `docs/benchmark/BENCHMARK_PLAN.md` |
| Public release legal checklist | P1 | `docs/release/PUBLICATION_STRATEGY.md` |

---

## 5. Inconsistencies (must resolve)

### 5.1 Phase taxonomy: five vs seven phases

| Source | Phase count | Notes |
|--------|-------------|-------|
| Literature foundation (Part 5.1) | **5 phases** (+ setup position) | Knee-angle ontology from Theia3D IJES 2025, Harbili & Alptekin |
| Thesis / current dataset | **7 classes** (+ unlabeled) | setup, first_pull, transition, second_pull, turnover, catch, recovery |
| Author clarifications (2026-07-13) | **7 classes** documented | Six-phase CV model (Cao et al., 2022; Chen et al., 2022) + Setup; see [`AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md) |

**Status:** Definitions **documented**; benchmark releases seven-class labels transparently. Manuscript must not claim full equivalence to the five-phase knee-angle standard without B0 mapping table. **Remaining:** implement B0 seven→five mapping (EXP-ONT).

### 5.2 Baseline model identity

| Source | Primary baseline |
|--------|------------------|
| Literature foundation | **B0 rule-based** + MS-TCN / ASFormer |
| Frozen repo baseline | **Window-level LSTM** (thesis reproduction) |
| Old `RESEARCH_ROADMAP.md` | GRU, TCN, ST-GCN as P0/P1 |

**Resolution:** LSTM remains **historical thesis baseline (frozen)** for reproduction only. **Benchmark baselines** follow literature tiers (B0–B3). Update roadmap references accordingly.

### 5.3 Task framing: classification vs segmentation

| Source | Framing |
|--------|---------|
| Thesis pipeline | Window classification (stride 1) |
| Literature foundation | Per-frame temporal action segmentation |
| Repo evaluation | Both supported in software; baseline uses windows only |

**Resolution:** Already partially documented. Benchmark must report segment + boundary metrics as primary; window metrics secondary (literature Part 3.3).

### 5.4 `docs/README.md` status line

States “No executable pipeline is fully ported yet” — **obsolete** after Phase 2 reproduction. Update to current status.

---

## 6. Duplicated information

| Content | Locations | Recommendation |
|---------|-----------|----------------|
| Reproduction summary | `REPRODUCTION_SUMMARY.md`, `research_design.md`, paper §5 | Keep summary canonical; others link |
| Metric definitions | `evaluation_metrics.md`, paper §5, external Part 3.3 | Single source: `evaluation_metrics.md` |
| Research roadmap | `audit/RESEARCH_ROADMAP.md`, literature Part 12, `BENCHMARK_PLAN.md` | **Supersede** audit roadmap with `BENCHMARK_PLAN.md`; mark audit copy historical |
| Figure/table plans | `figures_plan.md`, `tables_plan.md`, `WRITING_STATUS.md`, `PAPER_TODO.md` | `PAPER_TODO.md` for actions; plans for inventory |

---

## 7. Obsolete information

| Item | Location | Status |
|------|----------|--------|
| “No executable pipeline ported” | `docs/README.md` | Obsolete — fix |
| GRU as P0 submission blocker | `audit/RESEARCH_ROADMAP.md` | Superseded by literature-first benchmark plan |
| “Contribution = LSTM → modern models” without B0 | `research_design.md` §Future | Obsolete framing |
| OpenPose as recommended extractor | Literature only | Repo correctly uses MediaPipe; document as fixed extractor for benchmark v1 |

---

## 8. Recommended integration order

1. Reconcile phase ontology (student / biomechanics expert).
2. Implement B0 rule-based baseline specification + evaluation hooks.
3. Extend `boundary.py` for ms-level transition errors.
4. Add MS-TCN / ASFormer after checkpoint validation gate.
5. Populate Related Work from verified `[V]`/`[K]` citations only.
6. Run LOAO or grouped k-fold; update split documentation.

See [`../benchmark/BENCHMARK_PLAN.md`](../benchmark/BENCHMARK_PLAN.md) and [`../SCIENTIFIC_WORKFLOW.md`](../SCIENTIFIC_WORKFLOW.md).
