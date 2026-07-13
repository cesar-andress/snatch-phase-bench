# Paper TODO — manuscript action tracker

Extracted from the literature foundation, gap analysis, benchmark plan, and current manuscript state.

**Manuscript path:** `~/papers/snatch-phase-bench/paper/main.tex` (outside Git)  
**Writing status:** [`../../paper/WRITING_STATUS.md`](../../paper/WRITING_STATUS.md)  
**Location policy:** [`MANUSCRIPT_LOCATION.md`](MANUSCRIPT_LOCATION.md)  
**Reviewer risks:** [`REVIEWER_CHECKLIST.md`](REVIEWER_CHECKLIST.md)  
**External reference:** [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md)

---

## 1. Literature and citations

| ID | Action | Section affected | Blocker |
|----|--------|------------------|---------|
| LIT-01 | Verify all `[V]`/`[K]`/`[?]` entries from literature Part 9 before BibTeX | Related Work, Introduction | Manual DOI check |
| LIT-02 | Populate Related Work §2.1 markerless validity (Kanko, Theia3D, OpenCap) | §2 | **Done** (2026-07-13) |
| LIT-03 | Populate Related Work §2.2 skeleton encoders (ST-GCN, CTR-GCN, PoseC3D) | §2 | **Done** |
| LIT-04 | Populate Related Work §2.3 TAS (MS-TCN, ASFormer, DiffAct) | §2 | **Done** — expanded §2.4 |
| LIT-05 | Populate Related Work §2.4 sports phase segmentation (Sensors 2018 wearable) | §2 | **Done** — §2.5 |
| LIT-06 | Populate Related Work §2.5 weightlifting CV prior art table | §2, §3 | **Done** — `tab:prior_art_comparison` |
| LIT-07 | Add benchmarks & reproducibility subsection (PoseBench3D, OpenCap) | §2 | Partial — OpenCap cited; PoseBench3D pending |
| LIT-08 | Remove all `\todosource{...}` macros once real citations inserted | All | **Partial** — intro + §2 done; other sections remain |
| LIT-09 | Replace `@misc{todo_*}` placeholders in `bibliography.bib` | Bibliography | **Done** |

### Essential citations to verify first (literature Part 9 ESSENTIAL tier)

- MS-TCN, MS-TCN++, ASFormer, DiffAct
- ST-GCN, CTR-GCN, PoseC3D
- Kanko Theia3D validity; IJES 2025 snatch kinematics (phase ontology)
- Barbell-trajectory snatch (Springer 2025/2026)
- Breakfast, 50Salads, GTEA

---

## 2. Experiments (must complete before Results prose)

| ID | Experiment | Populates | Priority |
|----|------------|-----------|----------|
| EXP-01 | Validate `best_model.pt` checkpoint vs thesis JSON | `tab:baseline_reproduction` | **Done** (VERIFIED 2026-07-13) |
| EXP-02 | Implement B0 rule-based knee-angle baseline | `tab:benchmark_comparison` | **P0** |
| EXP-03 | Implement MS-TCN, MS-TCN++, ASFormer (**B2-core**) | `tab:benchmark_comparison` | **P0** |
| EXP-04 | Boundary MAE (ms) per phase transition | `tab:segment_metrics`, new boundary table | **P0** |
| EXP-05 | Segmental F1@10/25/50 + edit score for all models | `tab:segment_metrics` | P0 |
| EXP-06 | Grouped leave-one-athlete-out or k-fold | Results uncertainty columns | P1 |
| EXP-07 | Pose-extractor swap ablation | Robustness subsection | P1 |
| EXP-08 | Camera-angle / occlusion robustness | Discussion, appendix | P1 |
| EXP-09 | DiffAct + CTR-GCN/PoseC3D encoders (A1–A3) | Extended benchmark table | P2 |
| EXP-10 | Runtime analysis (params, FPS) | `tab:runtime` | P2 |
| EXP-11 | Inter-annotator agreement on boundary subset | Dataset §, Limitations | P1 |
| EXP-12 | Phase ontology documentation (5 vs 7 phases) | `tab:phase_taxonomy`, §3 | **Done** — [`AUTHOR_CLARIFICATIONS.md`](../reproduction/AUTHOR_CLARIFICATIONS.md); B0 mapping still P0 |

**Phase 3 design (2026-07-13):** Canonical specs in [`../benchmark/BENCHMARK_PROTOCOL.md`](../benchmark/BENCHMARK_PROTOCOL.md), [`EXPERIMENT_MATRIX.md`](../benchmark/EXPERIMENT_MATRIX.md), [`STATISTICAL_PROTOCOL.md`](../benchmark/STATISTICAL_PROTOCOL.md), [`BENCHMARK_GOVERNANCE.md`](../benchmark/BENCHMARK_GOVERNANCE.md). **No model implementation until design review sign-off.**

### Manuscript dependency map (benchmark milestones)

| Milestone | Experiments | Manuscript sections / artifacts |
|-----------|-------------|--------------------------------|
| M0 B1 verified | EXP-01 | §5 baseline protocol, `tab:baseline_reproduction`, `tab:baseline_perclass` |
| M1 Ontology | EXP-12 | §3–4, `tab:phase_taxonomy`, `fig:phase_illustration` |
| M2 B0 + metrics | EXP-02, EXP-04, EXP-MET | `tab:benchmark_comparison` (B0 row), `tab:boundary_*`, `tab:segment_metrics` |
| M3 B2-core | EXP-03, EXP-05, EXP-SEED | `tab:benchmark_comparison`, `fig:benchmark_comparison`, §6.2 |
| M4 Uncertainty | EXP-06 | §5 statistical testing prose, CI columns |
| M5 Discussion | DIS-01–03 | §7 after M2+M3 |
| M6 Runtime / ablation | EXP-10, EXP-ABL | `tab:runtime`, `tab:ablation` |
| M7 Robustness | EXP-07, EXP-08 | §7, appendices, `fig:error_analysis` |
| M8 IAA | EXP-11 | §3, §8 limitations |

---

## 3. Figures

| ID | Figure | Source | Status |
|----|--------|--------|--------|
| FIG-01 | Pipeline (3-stage: pose → encode → segment) | Redesign per literature Part 4.2 | Needs regeneration |
| FIG-02 | Dataset overview montage | Cleared exemplar videos | Future work |
| FIG-03 | Window vs dense segmentation contrast | Methods illustration | Placeholder |
| FIG-04 | Athlete-level split visualization | Split JSON + matplotlib | Needs regeneration |
| FIG-05 | Class distribution bar chart | Verified counts in `tab:class_distribution` | **Can generate now** |
| FIG-06 | Confusion matrix (baseline) | Checkpoint predictions | Blocked EXP-01 |
| FIG-07 | Training curves | `history.csv` | Needs regeneration |
| FIG-08 | Benchmark comparison bar/radar | EXP-03 results | Future work |
| FIG-09 | Boundary error per transition | EXP-04 | Future work |
| FIG-10 | Qualitative error analysis | Predictions + pose overlay | Blocked EXP-01 |
| FIG-11 | Prior-art comparison schematic | Related Work | **Done** — `fig:related_landscape` (TikZ) |

See also [`../figures_plan.md`](../figures_plan.md).

---

## 4. Tables

| ID | Table | Status | Blocker |
|----|-------|--------|---------|
| TAB-01 | Dataset statistics (extended metadata) | Partial | Legal + metadata |
| TAB-02 | Split statistics | **Verified** | None |
| TAB-03 | Class distribution | **Verified** | None |
| TAB-04 | Phase taxonomy + biomechanical definitions | Partial | EXP-12, expert review |
| TAB-05 | LSTM hyperparameters | **Verified** | None |
| TAB-06 | Baseline reproduction (checkpoint vs retrain) | **Verified** | None |
| TAB-07 | Per-class baseline metrics | **Verified** | None |
| TAB-08 | Benchmark comparison (all models) | Shell | EXP-02, EXP-03 |
| TAB-09 | Segment-level metrics | Shell | EXP-05 |
| TAB-10 | Boundary MAE per transition | **Not in manuscript yet** | EXP-04 — **add to §6** |
| TAB-11 | Ablation study | Shell | Ablation experiments |
| TAB-12 | Runtime comparison | Shell | EXP-10 |
| TAB-13 | Prior art comparison (weightlifting CV) | **`tab:prior_art_comparison` in §2** | LIT-06 — **done** 2026-07-13 |

See also [`../tables_plan.md`](../tables_plan.md).

---

## 5. Discussion topics (write after results)

| ID | Topic | Depends on |
|----|-------|------------|
| DIS-01 | Where learning beats B0 knee-angle rules (and where it does not) | EXP-02, EXP-04 |
| DIS-02 | Short-horizon TAS: does multi-stage refinement help? | EXP-03 |
| DIS-03 | Metric saturation vs boundary precision | EXP-04, EXP-05 |
| DIS-04 | Pose extractor sensitivity | EXP-07 |
| DIS-05 | Generalization across athletes | EXP-06 |
| DIS-06 | Comparison with barbell-trajectory and Theia3D prior art | LIT-06 |
| DIS-07 | Practical coaching implications (careful claims) | All above |
| DIS-08 | Threats to validity (internal/external/construct) | EXP-06, EXP-11 |

---

## 6. Limitations (expand when evidence available)

| ID | Limitation | Evidence today | Action |
|----|------------|----------------|--------|
| LIM-01 | Single cohort | Verified N=208/70 | Add demographics when available |
| LIM-02 | Monocular MediaPipe | Verified | Quantify pose error (EXP-04 context) |
| LIM-03 | Phase ontology vs biomechanics standard | Gap identified | EXP-12 |
| LIM-04 | No IAA | Verified absence | EXP-11 |
| LIM-05 | Checkpoint validated | Verified (2026-07-13) | Update limitations text — **done** |
| LIM-06 | Window overlap | Verified autocorrelation | Report segment metrics |
| LIM-07 | Benchmark incomplete | Verified | Update when EXP-02+ done |

---

## 7. Future work (manuscript §7 / §9)

Items to name but **not** execute in current submission (literature Part 11):

- Real-time coaching (OnlineTAS, latency budget)
- Weak / timestamp supervision for annotation cost
- Multi-view fusion for occlusion-robust catch
- 3D pose via MotionBERT / OpenCap pipeline
- Clean & jerk extension
- Injury-prevention linkage (clinical hook for JBHI/CMPB)
- Vision-language / foundation models (explicitly defer — novelty inflation risk)

---

## 8. Narrative / framing fixes

| ID | Action | File |
|----|--------|------|
| NAR-01 | Ensure abstract uses benchmark story sentence (literature Part 7.2) | `main.tex` |
| NAR-02 | Reframe contributions: dataset > benchmark > formalization > software | `01_introduction.tex` |
| NAR-03 | Add explicit “seam between three communities” gap paragraph | `02_related_work.tex` | **Done** |
| NAR-04 | Separate thesis LSTM from benchmark baselines in Methods | `04_methods.tex` |
| NAR-05 | Add boundary-ms metrics to Experimental Protocol | `05_experimental_protocol.tex` |
| NAR-06 | Add `tab:boundary_per_transition` placeholder to Results | `06_results.tex` |
| NAR-07 | Baseline Results numbers verified for checkpoint row only | `06_results.tex` | **Partial** — benchmark tables still pending |

---

## 9. Synchronization triggers

When any EXP-* completes:

1. Update external `~/papers/snatch-phase-bench/paper/WRITING_STATUS.md` completion %
2. Populate corresponding table/figure in LaTeX
3. Add one paragraph to Discussion outline
4. Update [`REVIEWER_CHECKLIST.md`](REVIEWER_CHECKLIST.md) status
5. Commit with message referencing experiment ID

See [`../SCIENTIFIC_WORKFLOW.md`](../SCIENTIFIC_WORKFLOW.md).

---

## 10. Priority queue (next 5 actions)

1. **EXP-12 / LIM-03** — Resolve phase ontology (blocks B0)
2. **EXP-MET + EXP-02** — Boundary metrics + B0 rule baseline
3. **EXP-03** — B2-core TAS models (MS-TCN → MS-TCN++ → ASFormer)
4. **EXP-04 / EXP-06** — Boundary tables + LOAO uncertainty
5. **EXP-B1-FIG** — Confusion matrix from checkpoint predictions

See [`RELATED_WORK_REVISION.md`](RELATED_WORK_REVISION.md) for the 2026-07-13 Section 2 rewrite log.
