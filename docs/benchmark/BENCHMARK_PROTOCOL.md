# SnatchPhaseBench — Benchmark Protocol (canonical specification)

**Version:** protocol-v1.0-draft  
**Status:** Phase 3 design (implementation **not** started)  
**Supersedes for scientific decisions:** operational details in [`BENCHMARK_PLAN.md`](BENCHMARK_PLAN.md) where conflicts arise — this document is canonical.

**Authoritative inputs (read-only):**

- [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md) Parts 3, 4, 6, 10, 12
- [`../research_design.md`](../research_design.md)
- [`BASELINE_SPECIFICATION.md`](BASELINE_SPECIFICATION.md) — frozen B1 LSTM
- [`../reproduction/CHECKPOINT_VALIDATION.md`](../reproduction/CHECKPOINT_VALIDATION.md)
- [`../evaluation_metrics.md`](../evaluation_metrics.md)
- [`../paper/REVIEWER_CHECKLIST.md`](../paper/REVIEWER_CHECKLIST.md)

**Related:**

- [`STATISTICAL_PROTOCOL.md`](STATISTICAL_PROTOCOL.md)
- [`BENCHMARK_GOVERNANCE.md`](BENCHMARK_GOVERNANCE.md)
- [`EXPERIMENT_MATRIX.md`](EXPERIMENT_MATRIX.md)

---

## 1. Benchmark objectives

SnatchPhaseBench evaluates **temporal phase segmentation of the Olympic snatch** from **fixed markerless pose inputs** under a **reproducible, athlete-disjoint protocol**.

| # | Objective | Journal defensibility |
|---|-----------|----------------------|
| O1 | Provide the first reproducible benchmark comparing learned temporal segmenters on identical inputs and splits, with documented biomechanical context | Answers Reviewer #1 (“why not knee-angle rules?”) via audit + exploratory B0 reference |
| O2 | Quantify performance with **boundary-level, millisecond-scale** metrics—not window accuracy alone | Mitigates metric saturation (Reviewer #7) |
| O3 | Report where learning **does and does not** improve over heuristics (occlusion, short phases, cross-athlete) | Honest benchmark positioning |
| O4 | Ship splits, preprocessing, metrics, and configs so independent groups can reproduce rankings | Reproducibility claim |
| O5 | Preserve the **verified thesis LSTM** as a frozen historical reference—not as the primary scientific competitor | Scientific honesty |

**Non-objectives (explicit):**

- Claiming a novel architecture or SOTA method contribution
- Real-time coaching deployment (deferred future work)
- Foundation-model novelty claims without controlled ablation

---

## 2. Benchmark philosophy

### 2.1 What this paper is

A **benchmark + dataset** paper for a biomechanically grounded, short-horizon temporal action segmentation task on skeleton sequences—not an applied-MS-TCN methods paper.

Defensible contributions (ranked; do not reorder):

1. Dataset (208 videos, 70 athletes, phase labels, athlete-disjoint split)
2. Benchmark protocol (preprocessing, metrics, baselines, code)
3. Domain formalization (boundary-ms evaluation tied to phase transitions)
4. Software artifact
5. New architecture — **not claimed**

### 2.2 Core scientific question

> Where do learned temporal segmenters improve over expert visual phase annotation on boundary timing—and how does that relate to biomechanical event vocabulary in the literature?

A negative result (learning does not beat expert labels on boundary timing) is **publishable** if boundary-level analysis is reported honestly.

### 2.3 Three-stage pipeline (roles must not blur)

```text
[Stage 1] Pose estimation     →  fixed keypoints (MediaPipe v1 for benchmark v1)
[Stage 2] Skeleton encoding   →  optional (raw / CTR-GCN / PoseC3D) — B2/B3 only
[Stage 3] Temporal segmentation → per-frame phase labels
```

- **ST-GCN, CTR-GCN** = encoders, not standalone segmenters
- **MS-TCN, ASFormer, DiffAct** = segmenters (B2)
- **MotionBERT, PoseFormer, VLMs** = upstream representations (B3; optional reach)

---

## 3. Fairness principles

| Principle | Rule |
|-----------|------|
| **Single preprocessing** | Identical keypoint CSV → tensor pipeline for all models on a given dataset version |
| **Single split file** | `athlete_split.json`; **clip-random splits forbidden** |
| **Single metric implementation** | `snatch_phase_bench.evaluation` for all models |
| **Fixed pose extractor (v1)** | MediaPipe Pose Landmarker (33 landmarks); extractor swaps are **robustness experiments**, not mixed into main table |
| **Train-only normalization** | Standardization statistics computed on training athletes only |
| **Documented training budget** | Max epochs, early-stopping criterion, and hyperparameter search budget per model family |
| **No test tuning** | Hyperparameters selected on validation split only |
| **Report failures** | If B2 underperforms on specific transitions, report it; do not hide per-transition boundary analysis |

---

## 4. Reproducibility principles

| Principle | Requirement |
|-----------|-------------|
| Config-as-code | Every run logged with YAML + git commit hash |
| Deterministic seeds | Documented in [`STATISTICAL_PROTOCOL.md`](STATISTICAL_PROTOCOL.md) |
| Artifact checksums | Dataset tensors, B1 checkpoint SHA-256 tracked |
| Prediction archives | Per-model test predictions stored under `outputs/benchmark/<model>/` |
| Environment pinning | `requirements-reproduction.txt` + `environment.json` per milestone |
| Read-only thesis snapshot | Never modified; canonical repo is sole write target |
| One-command reproduction | Target: `experiments/run_benchmark.py --config …` (post-implementation) |

---

## 5. Model inclusion and exclusion criteria

### 5.1 Inclusion criteria (main benchmark table)

A model **M** is included in the primary comparison (`tab:benchmark_comparison`) if:

1. It produces **per-frame** phase labels on the full test set (B0, B2) **or** is the frozen **B1** checkpoint evaluated under its verified window protocol.
2. It uses **Stage-1 keypoints** from the benchmark v1 extractor without external pose sources.
3. It is trained only on **train athletes**; validated on **val**; evaluated once on **test**.
4. Its training recipe is **fully documented** (YAML + paper appendix).
5. Predictions pass automated shape/consistency tests.

### 5.2 Exclusion criteria

| Excluded | Reason |
|----------|--------|
| Clip-random or video-random splits | Athlete leakage |
| Models trained on test athletes | Invalid comparison |
| Per-test hyperparameter tuning | Optimistic bias |
| Window-only models without frame/segment export (except B1 row) | Cannot compute primary endpoints |
| ST-GCN alone without TAS head | Wrong task (recognition ≠ segmentation) |
| VLMs / foundation models without controlled pose input | Confounds Stage 1; B3 appendix only |
| HD-GCN, InfoGCN, exhaustive GCN zoo | Excessive for 5–7 phases; cite, do not run all |
| GRU matched to LSTM | Ablation only (`tab:ablation`), not main table |

### 5.3 Trivial baselines (mandatory anchors)

Report alongside B2 models (appendix or table footer):

- Majority class
- Persistence (previous-frame phase)
- Phase-frequency prior (train distribution)

Purpose: prove learned models exceed trivial predictors.

---

## 6. Reporting policy

### 6.1 Metric ordering in all primary tables

1. **Boundary MAE (ms)** — aggregated and per-transition
2. **Boundary within-τ (%)** — τ ∈ {1, 2, 3} frames
3. **Segmental F1@50** (then @25, @10)
4. **Edit score**
5. **Frame accuracy (MoF)**
6. **Window-level metrics** — B1 only; appendix or secondary column for others if applicable

### 6.2 Required reporting elements per model

- Point estimate + uncertainty (see statistical protocol)
- Per-class / per-phase recall for short phases (`transition`, `second_pull`)
- Per-transition boundary table (`tab:boundary_per_transition`)
- Parameter count, inference latency (see §9)
- Config hash and seed list

### 6.3 Narrative policy

- Never claim “our method beats biomechanics” without B0 numbers
- Never claim SOTA without segment + boundary evidence
- Separate **B1 thesis reproduction** from **B2 TAS benchmark** in prose
- All numbers in manuscript must trace to committed `outputs/benchmark/` JSON

---

## 7. Benchmark hierarchy

**Canonical tier naming (Phase 3):** supersedes legacy labels in older docs where B1 referred to MS-TCN.

| Tier | Name | Role | Status |
|------|------|------|--------|
| **B0** | Knee-angle exploratory reference | **Exploratory only** — documents biomechanical event vocabulary; audit concluded knee-only implementation unsupported | **FROZEN** (no code) |
| **B1** | Frozen thesis LSTM (window classifier) | **Historical reference** — reproduction verified | **VERIFIED** |
| **B2** | Modern temporal segmentation architectures | **Primary learned comparators** (MS-TCN family, ASFormer, DiffAct) | Infrastructure ready (MS-TCN stub) |
| **B3** | Foundation-model / representation approaches | Optional reach (MotionBERT, PoseFormer, encoder+TAS) | Future / appendix |

### 7.1 B0 status (2026-07-14)

The biomechanical evidence audit ([`B0_EVIDENCE_MATRIX.md`](B0_EVIDENCE_MATRIX.md)) concluded that a knee-angle-only rule segmenter cannot be implemented without unsupported assumptions. **B0 is frozen as an exploratory reference**, not a primary benchmark row. See [`B0_EXPLORATORY_REFERENCE.md`](B0_EXPLORATORY_REFERENCE.md).

Reviewers asking “why not knee-angle rules?” are answered by the audit (what literature names vs what fixed pose inputs observe) and by comparing learned segmenters to **expert labels** on boundary timing—not by a fabricated rule baseline.

### 7.2 Why B1 exists

B1 preserves **exact reproducibility of prior thesis work** (checkpoint SHA-256 verified). It anchors window-level metrics but **must not** be the only learned baseline in the benchmark story.

### 7.3 Why B2 exists

MS-TCN, ASFormer, and successors are the **standard TAS baselines** in the computer vision literature. SnatchPhaseBench must compare against them under identical inputs—not only against an LSTM window classifier.

**B2 mandatory set (main table):**

| Model | Registry (planned) | Rationale |
|-------|-------------------|-----------|
| MS-TCN | `ms_tcn` | Canonical TAS baseline |
| MS-TCN++ | `ms_tcn_pp` | Refinement stages ablation built-in |
| ASFormer | `asformer` | Strong attention segmenter |

**B2 recommended extensions:**

| Model | Priority | Rationale |
|-------|----------|-----------|
| DiffAct | P1 | Advanced generative TAS |
| CTR-GCN → TAS head | P1 | Tests whether graph encoder helps short motion |
| PoseC3D → TAS head | P2 | Representation contrast |

### 7.4 Why B3 exists

Foundation pose models (MotionBERT, PoseFormer) and VLMs represent a **future compatibility lane**. They are **not** required for a Q1 benchmark submission but document upgrade path and reviewer-proof breadth if included as appendix.

**B3 policy:** Include only after B2 mandatory set complete; never mix unfixed upstream representations into the primary table without ablation.

---

## 8. Scientific questions by experiment

Each experiment follows: **Question → Hypothesis → Evidence → Success criterion → Statistics → Figures → Tables**.

Full matrix with priorities and estimates: [`EXPERIMENT_MATRIX.md`](EXPERIMENT_MATRIX.md).

### EXP-B0 — Knee-angle exploratory reference (frozen)

| Field | Specification |
|-------|---------------|
| **Question** | What biomechanical events does validation literature use to name pull phases, and which are observable from fixed MediaPipe pose alone? |
| **Outcome (2026-07-14)** | Audit accepted; **no rule-based implementation**. Middle-pull knee events partially named in literature; setup and overhead transitions require non-pose cues. |
| **Artifacts** | [`B0_EVIDENCE_MATRIX.md`](B0_EVIDENCE_MATRIX.md), [`B0_EXPLORATORY_REFERENCE.md`](B0_EXPLORATORY_REFERENCE.md) |
| **Manuscript role** | Methods/Discussion cite audit; **not** a competitive benchmark row |

### EXP-B1 — Thesis reference (complete)

| Field | Specification |
|-------|---------------|
| **Question** | Does the original thesis checkpoint reproduce under canonical evaluation? |
| **Hypothesis** | Exact match to saved classification report. |
| **Evidence** | [`CHECKPOINT_VALIDATION.md`](../reproduction/CHECKPOINT_VALIDATION.md) |
| **Success criterion** | **MET** — all metrics EXACT. |
| **Statistics** | None (deterministic checkpoint eval). |
| **Figures** | `fig:confusion_matrix` (from checkpoint predictions). |
| **Tables** | `tab:baseline_reproduction`, `tab:baseline_perclass` |

### EXP-B2-CORE — TAS benchmark core

| Field | Specification |
|-------|---------------|
| **Question** | Do standard TAS architectures improve boundary timing and segment-F1 over B0 and B1? |
| **Hypothesis** | B2 models improve short-phase recall and Second Pull→Turnover boundary MAE; gains may be modest on long phases. |
| **Evidence required** | MS-TCN, MS-TCN++, ASFormer trained under frozen recipe; identical splits. |
| **Success criterion** | All three models complete training; primary metrics reported with uncertainty. |
| **Statistics** | 3–5 seeds; bootstrap CI; paired Wilcoxon vs B0 on per-video boundary MAE; Holm correction. |
| **Figures** | `fig:benchmark_comparison`; `fig:boundary_per_transition`. |
| **Tables** | `tab:benchmark_comparison`, `tab:segment_metrics`, `tab:boundary_metrics` |

### EXP-B2-EXT — Advanced B2 contrasts

| Field | Specification |
|-------|---------------|
| **Question** | Do DiffAct or skeleton encoders materially change rankings? |
| **Hypothesis** | Diminishing returns on 2–6 s single-athlete motion; encoders may not justify complexity. |
| **Evidence** | DiffAct; CTR-GCN+TAS optional. |
| **Success criterion** | Reported in extended table or appendix; does not block submission if omitted. |
| **Statistics** | Same as EXP-B2-CORE. |
| **Figures** | Optional extended benchmark figure. |
| **Tables** | `appendices/D_benchmark_extra` |

### EXP-MET — Metric infrastructure

| Field | Specification |
|-------|---------------|
| **Question** | Are boundary-ms and segment-F1 implemented consistently for all models? |
| **Hypothesis** | Unified evaluator removes metric implementation bias. |
| **Evidence** | `boundary.py` + tests; golden files on B1 aggregated predictions. |
| **Success criterion** | All primary metrics computable from any model's test predictions. |
| **Statistics** | Unit tests; no inferential stats. |
| **Figures** | — |
| **Tables** | Enables all results tables |

### EXP-SPLIT — Uncertainty across athletes

| Field | Specification |
|-------|---------------|
| **Question** | How stable are rankings across athlete groupings? |
| **Hypothesis** | Single 49/10/11 split is optimistic/pessimistic for some models; LOAO widens CIs. |
| **Evidence** | Grouped leave-one-athlete-out (LOAO) or k-fold on athletes. |
| **Success criterion** | Mean ± SD reported for primary metrics; rank correlation reported. |
| **Statistics** | Bootstrap over athletes; report 95% CI. |
| **Figures** | Split variance chart. |
| **Tables** | Supplementary uncertainty columns |

### EXP-ROB-POSE — Extractor sensitivity

| Field | Specification |
|-------|---------------|
| **Question** | Do rankings depend on MediaPipe vs alternatives? |
| **Hypothesis** | Metric shifts ≤ few pp; boundary MAE at catch most sensitive. |
| **Evidence** | Re-run Stage 1 with HRNet or RTMPose on subset or full set. |
| **Success criterion** | Documented variance; benchmark v1 remains MediaPipe. |
| **Statistics** | Paired comparison on matched frames. |
| **Figures** | Robustness bar chart. |
| **Tables** | Appendix robustness table |

### EXP-ROB-CAM — Camera / occlusion

| Field | Specification |
|-------|---------------|
| **Question** | Do models generalize across camera angles and occlusions? |
| **Hypothesis** | Oblique views hurt B0 and B2; catch occlusion hurts all. |
| **Evidence** | Stratified eval by metadata tags (when available). |
| **Success criterion** | Honest limitation if metadata incomplete; partial stratification acceptable. |
| **Statistics** | Descriptive strata; Fisher exact for failure modes. |
| **Figures** | `fig:error_analysis` |
| **Tables** | Error analysis appendix |

### EXP-ABL — Ablations

| Field | Specification |
|-------|---------------|
| **Question** | Which input/window/hyper choices drive performance? |
| **Hypothesis** | Window length and visibility features matter; MS-TCN stages help over-segmentation. |
| **Evidence** | Controlled single-factor changes on MS-TCN. |
| **Success criterion** | At least window length + visibility ablations for submission-strengthening. |
| **Statistics** | Paired on same seed. |
| **Figures** | — |
| **Tables** | `tab:ablation` |

### EXP-ONT — Phase ontology

| Field | Specification |
|-------|---------------|
| **Question** | Can seven thesis phases be mapped to five-phase biomechanics standard? |
| **Hypothesis** | Mapping exists with documented merge rules; affects B0 threshold design. |
| **Evidence** | Expert review + mapping table. |
| **Success criterion** | Operational definitions in `tab:phase_taxonomy`; B0 uses reconciled events. |
| **Statistics** | None pre-implementation. |
| **Figures** | `fig:phase_illustration` |
| **Tables** | `tab:phase_taxonomy` |

### EXP-IAA — Inter-annotator agreement

| Field | Specification |
|-------|---------------|
| **Question** | How much label noise exists at boundaries? |
| **Hypothesis** | Boundary disagreement ≤ X frames for Y% of transitions (to be measured). |
| **Evidence** | Second annotator on ≥50 attempts subset. |
| **Success criterion** | κ or boundary MAE between annotators reported. |
| **Statistics** | Cohen's κ; frame-tolerant boundary agreement. |
| **Figures** | — |
| **Tables** | Dataset § + limitations |

### EXP-RT — Runtime and efficiency

| Field | Specification |
|-------|---------------|
| **Question** | What is the cost of each tier? |
| **Hypothesis** | B0 cheapest; B2 moderate; B3 expensive. |
| **Evidence** | Params, GPU/CPU latency, training wall-clock on standardized hardware. |
| **Success criterion** | `tab:runtime` populated for B0, B1, B2-core. |
| **Statistics** | Descriptive only. |
| **Figures** | Optional efficiency scatter. |
| **Tables** | `tab:runtime` |

### EXP-B3 — Foundation models (optional)

| Field | Specification |
|-------|---------------|
| **Question** | Do frozen pose representations improve segmentation? |
| **Hypothesis** | Gains limited when Stage-1 is fixed monocular 2D. |
| **Evidence** | MotionBERT/PoseFormer features → TAS head. |
| **Success criterion** | Appendix-only; does not block v1 submission. |
| **Statistics** | Same as B2 if run. |
| **Figures** | Appendix. |
| **Tables** | Extended benchmark appendix |

---

## 9. Evaluation protocol (design only)

### 9.1 Data flow

```text
keypoints CSV + frame labels + athlete_split.json
        ↓
[preprocessing — frozen dataset version]
        ↓
model → per-frame label sequence (test athletes only)
        ↓
snatch_phase_bench.evaluation.{frame,segment,boundary,window}
        ↓
reports JSON + manuscript tables
```

### 9.2 Window-level metrics (B1 primary; secondary elsewhere)

| Metric | Definition | Module | Use |
|--------|------------|--------|-----|
| Accuracy | Correct window center label | `window.py` | B1 reproduction |
| Macro P/R/F1 | Unweighted class mean | `window.py` | B1, diagnostic |
| Weighted F1 | Support-weighted | `window.py` | B1 |
| Per-class P/R/F1 | Per phase | `window.py` | `tab:baseline_perclass` |

**Policy:** Do not lead with window metrics in abstract; stride-1 overlap violates independence (see [`../reproduction/temporal_autocorrelation.md`](../reproduction/temporal_autocorrelation.md)).

### 9.3 Frame-level metrics

| Metric | Definition | Module |
|--------|------------|--------|
| Frame accuracy (MoF) | Per-frame label equality after window aggregation or dense prediction | `frame.py` |
| Macro / weighted F1 | As above on frames | `frame.py` |

**Aggregation rule (window models):** majority vote at each frame from overlapping windows; document tie-breaking.

### 9.4 Segment-level metrics

| Metric | Definition | Module |
|--------|------------|--------|
| Segmental F1@10/25/50 | IoU threshold τ ∈ {0.10, 0.25, 0.50} | `segment.py` |
| Edit score | Normalized Levenshtein on segment sequences | `segment.py` |
| Per-phase segment recall | Short-phase collapse diagnostic | extend reports |

### 9.5 Boundary metrics (primary endpoint)

| Metric | Definition | Module |
|--------|------------|--------|
| Boundary MAE (frames) | \|t* − t̂\| per transition | `boundary.py` (TODO) |
| Boundary MAE (ms) | MAE × 1000/fps | `boundary.py` (TODO) |
| Within-τ (%) | Fraction within ±1,2,3 frames | `boundary.py` (TODO) |
| Per-transition MAE | Six transitions (seven-phase ontology) | `boundary.py` (TODO) |

**Priority transition:** Second Pull → Turnover (literature + class difficulty).

### 9.6 Runtime and resource metrics

| Metric | Measurement | Hardware |
|--------|-------------|----------|
| Parameter count | Model.summary / torch | — |
| Model size (MB) | Checkpoint file | — |
| Training time | Wall-clock train+val to early stop | 1× reference GPU + log CPU |
| Inference speed | ms/video and FPS (pose excluded vs end-to-end) | Same reference |
| Peak memory | Max GPU/CPU RSS during inference | Same reference |

Reference hardware document: single NVIDIA GPU (model TBD at implementation) + Apple/Linux CPU fallback for B0/B1.

### 9.7 Split protocols

| Protocol | Role |
|----------|------|
| Fixed 49/10/11 athlete holdout | **Primary reported split** (verified) |
| Grouped LOAO | **Mandatory uncertainty extension** |
| Clip-random | **Forbidden** |

---

## 10. Publication roadmap

### 10.1 Mandatory for submission (Sensors / BSPC)

| ID | Deliverable | Milestone |
|----|-------------|-----------|
| P-M1 | Phase ontology reconciliation | EXP-ONT |
| P-M2 | B0 + boundary metric implementation | EXP-B0 + EXP-MET |
| P-M3 | B2-core (MS-TCN, MS-TCN++, ASFormer) | EXP-B2-CORE |
| P-M4 | Primary results tables + boundary figures | Manuscript §6 |
| P-M5 | Statistical uncertainty (seeds or LOAO) | EXP-SPLIT |
| P-M6 | Verified citations + honest limitations | LIT-* |
| P-M7 | Legal clearance or documented video restriction | Release |

### 10.2 Strengthens paper (recommended)

| ID | Deliverable |
|----|-------------|
| P-S1 | Trivial baselines + per-transition breakdown |
| P-S2 | Ablations (window, visibility) |
| P-S3 | Confusion matrix + error analysis figure |
| P-S4 | Runtime table |
| P-S5 | EXP-IAA subset study |

### 10.3 Optional / appendix

| ID | Deliverable |
|----|-------------|
| P-O1 | DiffAct, CTR-GCN+TAS |
| P-O2 | Pose-extractor swap |
| P-O3 | Camera/occlusion stratification |
| P-O4 | B3 foundation models |

### 10.4 Future work (name only in Discussion)

- OnlineTAS / real-time coaching
- Weak supervision
- Multi-view capture
- Clean & jerk extension
- Zenodo public video release (when legal)

---

## 11. Implementation order (scientific value × effort)

**Do not sort by coding difficulty alone.** Recommended sequence:

| Step | Work | Rationale |
|------|------|-----------|
| **1** | EXP-ONT (ontology) | **Done** |
| **2** | EXP-MET (`boundary.py` + tests) | **Done** — primary endpoint |
| **3** | EXP-B0 audit | **Done** — frozen exploratory reference |
| **4** | MS-TCN infrastructure | **Done** — adapters, hooks, config stub |
| **5** | EXP-B2-CORE (MS-TCN → MS-TCN++ → ASFormer) | Main scientific comparison |
| **6** | Experiment runner + prediction archives | Unblocks benchmark runs |
| **7** | EXP-SPLIT (LOAO) | Uncertainty for claims |
| **8** | Manuscript population §6 + Discussion | Publication path |
| **9** | EXP-RT (runtime) | Low risk, fills `tab:runtime` |
| **10** | EXP-ABL / EXP-IAA / robustness | Optional enrichment |

B1 evaluation and figures can proceed in **parallel with step 1** (no implementation).

---

## 12. Reviewer #2 critical review (design stage)

| Criticism | Severity | Mitigation in this protocol |
|-----------|----------|----------------------------|
| “Why not knee-angle rules?” | **Addressed by audit** | B0 frozen as exploratory reference; compare B2 to expert labels + cite literature event vocabulary |
| “Applied TAS, no novelty” | High | Benchmark framing; boundary-ms formalization |
| “Dataset too small” | Medium | Athlete-disjoint eval; honest N; LOAO uncertainty |
| “Pose bad at catch” | Medium | Per-transition boundary table; occlusion discussion |
| “Clip leakage” | Low (if protocol followed) | Athlete split enforced; CI test |
| “MediaPipe arbitrary” | Medium | Fixed v1 + robustness appendix plan |
| “Accuracy saturates” | High | Primary endpoints = boundary + segment-F1 |
| “Not reproducible” | Low post-validation | B1 verified; governance doc; Zenodo plan |
| “Single annotator” | Medium | EXP-IAA; biomechanical definitions |
| “Seven vs five phases” | **High** | EXP-ONT before B0 finalize |
| “Window overlap inflates p-values” | Medium | Segment/boundary unit; statistical protocol |
| “Weak baselines” | Medium | B0 + trivial baselines + MS-TCN family |
| “Missing statistical tests” | Medium | [`STATISTICAL_PROTOCOL.md`](STATISTICAL_PROTOCOL.md) |
| “Unfair tuning” | Medium | Frozen budget per family; val-only selection |
| “No runtime / deployment” | Low | `tab:runtime` in recommended set |

---

## 13. Open decisions (require resolution before implementation)

| ID | Decision | Options | Owner / blocker |
|----|----------|---------|-----------------|
| OD-1 | Seven-phase vs mapped five-phase for B0 | Keep 7 / merge to 5 / dual reporting | Domain expert (EXP-ONT) |
| OD-2 | B0 knee-angle operational definition | Exact joint triple + thresholds | Biomechanics + EXP-ONT |
| OD-3 | LOAO vs k-fold on athletes | LOAO primary; k=5 optional | Statistical power |
| OD-4 | Number of random seeds | 3 minimum, 5 recommended | Compute budget |
| OD-5 | Early-stop metric for B2 | Val macro-F1 vs segment-F1@50 | Pilot on MS-TCN |
| OD-6 | Reference GPU for runtime | Document available hardware | Lab infra |
| OD-7 | Video public release scope | Full / keypoints-only / restricted | Legal |

---

## 14. Manuscript mapping

| Benchmark milestone | Manuscript anchor |
|--------------------|-------------------|
| B1 verified | `tab:baseline_reproduction`, `tab:baseline_perclass`, §5 baseline protocol |
| EXP-ONT | `tab:phase_taxonomy`, §3–4 Methods |
| EXP-MET + B0 + B2 | `tab:benchmark_comparison`, `tab:segment_metrics`, `tab:boundary_metrics`, `tab:boundary_per_transition` |
| EXP-SPLIT | Uncertainty columns; §5 statistical testing |
| EXP-RT | `tab:runtime` |
| EXP-ABL | `tab:ablation` |
| EXP-ROB | §7 Discussion, appendices |
| EXP-IAA | §3 Dataset, §8 Limitations |

See [`../paper/PAPER_TODO.md`](../paper/PAPER_TODO.md) and external `~/papers/snatch-phase-bench/paper/WRITING_STATUS.md`.

---

## 15. Document history

| Version | Date | Change |
|---------|------|--------|
| protocol-v1.0-draft | 2026-07-13 | Phase 3 canonical benchmark design |
