# Remaining blockers — post checkpoint validation

**Updated:** 2026-07-13  
**Context:** Thesis LSTM checkpoint **VERIFIED** (all metrics EXACT). Baseline reproduction phase **closed**.

Ranked by **scientific importance** (highest first).

---

## 1. Phase ontology reconciliation (7 vs 5 phases)

**Impact:** High — affects biomechanical interpretability, prior-art comparison, and rule-based B0 design.

**Evidence:** Thesis uses seven labels (`setup`, `first_pull`, `transition`, `second_pull`, `turnover`, `catch`, `recovery`); IJES 2025 snatch kinematics and coaching literature often collapse to five phases. `tab:phase_taxonomy` lists names without operational definitions.

**Status:** Unresolved (EXP-12).

---

## 2. Benchmark tiers B0–B3 not implemented

**Impact:** High — core SnatchPhaseBench contribution is comparative evaluation; only thesis LSTM is validated.

**Evidence:** [`BENCHMARK_PLAN.md`](../benchmark/BENCHMARK_PLAN.md) — B0 rule-based, B1–B3 TAS models marked “Not implemented”.

**Status:** Gate for checkpoint passed; implementation not started.

---

## 3. Segment- and boundary-level metrics

**Impact:** High — window-level accuracy is secondary endpoint; boundary MAE (ms) is the planned primary benchmark metric.

**Evidence:** `tab:segment_metrics`, `tab:boundary_metrics` are placeholders; no frame/segment inference pipeline results committed.

**Status:** Blocked on B0+ model implementations and dense prediction export.

---

## 4. Frame count discrepancy (37,125 vs 35,825)

**Impact:** Medium-high — affects trust in dataset documentation if unexplained.

**Evidence:** Phase 1 audit vs thesis narrative; rebuilt tensors match manifest (21,249 windows) but raw frame accounting differs.

**Status:** Requires student/source clarification; does not affect validated checkpoint metrics.

---

## 5. Inter-annotator agreement undocumented

**Impact:** Medium — reviewers will ask about label reliability.

**Evidence:** Limitations §; no κ or boundary-error study on annotation subset.

**Status:** EXP-11 planned.

---

## 6. Legal / licensing / public release

**Impact:** Medium — blocks Zenodo DOI and external reproducibility.

**Evidence:** Athlete identifiers in paths; `Public Zenodo DOI` pending in reproducibility appendix.

**Status:** Legal review required.

---

## 7. Camera metadata and robustness

**Impact:** Medium — generalization claims need FPS, resolution, angle diversity.

**Evidence:** `tab:dataset_stats` — native FPS/resolution pending; oblique-camera robustness rows are placeholders.

**Status:** Metadata collection + EXP-08.

---

## 8. Publication figures (confusion matrix, training curves)

**Impact:** Low-medium — metrics verified; visualization export pending.

**Evidence:** `fig:confusion_matrix`, `fig:training_curves` still placeholders; predictions not yet plotted.

**Status:** Can generate from checkpoint eval outputs.

---

## 9. Statistical testing protocol

**Impact:** Low-medium — needed before claiming significant differences between models.

**Evidence:** §5 statistical testing marked planned.

**Status:** After benchmark runs complete.

---

## Resolved (no longer blockers)

| Item | Resolution |
|------|------------|
| Missing `best_model.pt` binary | Recovered at snapshot root; SHA matches manifest |
| Exact checkpoint evaluation | **VERIFIED** 2026-07-13 |
| LFS pointer at `outputs/lstm_phases/best_model.pt` | Bypassed via canonical copy |

---

## Recommended next milestone

**M2** per benchmark plan: implement **B0 rule-based** baseline + boundary metrics on the frozen split and dataset version.
