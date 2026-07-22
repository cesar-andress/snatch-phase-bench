# Figure audit — SnatchPhaseBench manuscript

**Date:** 2026-07-22  
**Scope:** Figures **included in the LaTeX build** (`main.tex` → section `\input`s).  
**Assets inspected:** TikZ `fig_related_landscape`; PNGs under `paper/figures/generated/asformer_b3/` (150 dpi Matplotlib exports).  
**Policy:** Recommend keep / redo / remove. No scientific numbers changed in this audit.

---

## Inventory (in build)

| Label | File | Placement | Asset |
|-------|------|-----------|-------|
| `fig:related_landscape` | `figures/fig_related_landscape.tex` | Related Work | TikZ |
| `fig:benchmark_comparison` | `figures/fig_benchmark_comparison.tex` | Results §Benchmark | `aggregate_seed_stability.png` (ASFormer only) |
| `fig:confusion_matrix` | `figures/fig_confusion_matrix.tex` | Results §ASFormer | `confusion_matrix_seed42.png` |
| `fig:training_curves` | `figures/fig_training_curves.tex` | Results §ASFormer | `training_curves_seed42.png` |
| `fig:error_analysis` | `figures/fig_error_analysis.tex` | Results §Qualitative | `qualitative_timeline_seed42.png` |

**Not in build** (orphan wrappers from prior placeholder pass; excluded from scoring):  
`fig_dataset_overview`, `fig_phase_illustration`, `fig_pipeline`, `fig_split_visualization`, `fig_class_distribution`, `fig_window_construction`, `fig_boundary_per_transition`.

---

## Checklist summary

| Criterion | Landscape | Benchmark bars | Confusion | Training curves | Qualitative timeline |
|-----------|:---------:|:--------------:|:---------:|:---------------:|:--------------------:|
| Referenced before appearance | Yes | **No** | **No** | **No** | **No** |
| Publication quality | Pass | Fail | Marginal | Fail | Marginal |
| Readable in print | Pass | Marginal | Marginal | Fail | Marginal |
| Axis labels | N/A (diagram) | **Y missing** | Present | **Missing** | Present |
| Units | N/A | **Mixed / unclear** | Colorbar unit missing | **Missing** | Frame OK; unlabeled class unlabeled |
| Consistent font size | Pass | Matplotlib default | Same | Same | Same (small) |
| Consistent terminology | Pass | **snake_case keys** | **snake_case** | Shorthand OK | **snake_case** + raw path title |
| Caption ≤ 2–3 sentences | 2 (dense) | 2–3 | 2 | 1–2 | **3 + Results echo** |
| Caption ≠ Results dump | Pass | Pass | Pass | Pass | **Fail** |
| Substantially improves understanding | Marginal | **No** | Yes (if cited) | **No** | Yes (if cleaned) |
| **Verdict** | **Keep (optional trim)** | **Remove or replace** | **Keep after redo + cite** | **Remove** | **Keep after redo + cite** |

---

## Per-figure findings

### 1. `fig:related_landscape` (TikZ)

**Reference order.** `\Cref{fig:related_landscape}` appears in Related Work *before* `\input` — **pass**.

**Quality / print.** Vector TikZ; fonts `\small`/`\footnotesize`; prints cleanly.

**Axes / units.** Conceptual diagram — N/A.

**Terminology.** Aligns with section vocabulary (marker-based → markerless → skeleton → TAS → benchmark).

**Caption.** Two sentences; slightly encyclopedic (“Pose estimation supplies…”) but does not dump Results.

**Redundancy.** Overlaps prose one paragraph earlier; still useful as a visual TOC for the section.

**Recommendation.** **Keep.** Optionally shorten caption to one sentence:  
*“Dependency chain from instrumented biomechanics to the SnatchPhaseBench protocol.”*  
Do not expand into a second landscape figure.

---

### 2. `fig:benchmark_comparison` (`aggregate_seed_stability.png`)

**Reference order.** Float is `\input` under Results §Benchmark, but the text only cites `tab:benchmark_comparison`. Figure is an **orphan float** — **fail**.

**Quality / print.** 1200×600 @ 150 dpi — thin for two-column print; rotated snake_case x-tick labels will shrink further.

**Axis labels / units.** No y-axis label. Five metrics on one 0–1 scale; `boundary_mae_frames` is in **frames** (lower better) while F1/edit are unitless (higher better). Caption does not warn about dual polarity.

**Terminology.** Plot uses JSON keys (`segmental_f1_at_50`, `frame_macro_f1`) vs manuscript “segment F1@50”, “frame macro-F1”.

**Caption.** Mentions ASFormer seed stability and file provenance (`test_metrics_aggregate.json`) — third sentence is production noise, not reader value. Placement under “Benchmark comparison” (B2 vs B3) while showing **only B3** is misleading.

**Redundancy.** Fully superseded by `tab:mstcn_seed_stability` + `tab:asformer_b3` / `tab:asformer_seed_stability` and the comparison table. Bars add no cross-model comparison.

**Recommendation.** **Remove from the manuscript.**  
If a visual comparison is required later, replace with a **grouped B2 vs B3** bar/dot plot (separate panel or twin axis for MAE), publication labels, ≥300 dpi, and a `\Cref` in §Benchmark *before* the float.

---

### 3. `fig:confusion_matrix` (`confusion_matrix_seed42.png`)

**Reference order.** Included under §ASFormer with **no** `\Cref{fig:confusion_matrix}` anywhere in body — **fail**.

**Quality / print.** 1050×900 @ 150 dpi; diagonal readable; off-diagonal catch/turnover confusions visible. For print, regenerate at ≥300 dpi and prefer PDF/vector.

**Axis labels / units.** “True” / “Predicted” present. Colorbar lacks a title (e.g. “Frame count”). In-figure title duplicates caption.

**Terminology.** Phase names in `snake_case`; manuscript mixes `texttt` snake_case and prose — acceptable if caption states “class names as in the frozen ontology,” but Title Case or short labels print better.

**Caption.** Two sentences; informative; does not restate numeric Results. Does not note that `unlabeled` is excluded from the plotted 7×7 (caption says eight-class ontology — slight mismatch with the 7×7 panel).

**Understanding.** Adds value beyond per-class recall tables by showing **which** confusions dominate.

**Recommendation.** **Keep after production redo:** cite in §ASFormer or §Qualitative *before* the figure; colorbar title; drop in-plot title; fix ontology wording; bump dpi. Optional: add MS-TCN panel only if space allows (not required).

---

### 4. `fig:training_curves` (`training_curves_seed42.png`)

**Reference order.** Not cited — **fail**.

**Quality / print.** Diagnostic Matplotlib dual panel; missing **x** (“Epoch”) and **y** labels on both axes; titles embed “seed 42”. Val segment F1@50 is noisy without marking the selected best epoch — hard to interpret in print.

**Understanding.** Does not improve scientific claims already covered by early-stopping narrative and seed tables. Single-seed curves are not the paper’s contribution.

**Caption.** Concise; still cannot rescue missing axes.

**Recommendation.** **Remove from main text.** If retained at all, move to an appendix with axis labels, best-epoch marker, and multi-seed overlay — otherwise omit.

---

### 5. `fig:error_analysis` (`qualitative_timeline_seed42.png`)

**Reference order.** Float appears at start of §Qualitative; prose after it never `\Cref`s the figure — **fail** (should cite before or in the first sentence).

**Quality / print.** 1800×450 @ 150 dpi; wide aspect may become unreadably short when width-constrained. In-plot title contains an **internal video path** (`bardalez/snatch_-65kg_...mp4`) — not publication-ready.

**Axis labels / units.** X: “Frame” (good). Y: phase categories (good). GT line occupies an unlabeled level below `setup` (`unlabeled` / background) — readers cannot name that state.

**Terminology.** snake_case phases; legend “ground truth” / “prediction” OK.

**Caption.** Three sentences; **sentence 2–3 repeat** §Boundary / §Qualitative prose (`transition`/`turnover`, `catch`→`recovery`) — violates “do not repeat Results.”

**Understanding.** Best current qualitative evidence of lagging boundaries; worth keeping if cleaned.

**Recommendation.** **Keep after redo:** anonymize title (e.g. “Test video, seed 42”); label `unlabeled`; enlarge fonts; ≥300 dpi; shorten caption to ≤2 sentences without restating MAE numbers; add `\Cref{fig:error_analysis}` in the first qualitative sentence.

---

## Proposed figure (not yet in manuscript)

### Catch → recovery qualitative inset

**Why.** Highest per-transition MAE is `catch`→`recovery` (MS-TCN 4.52 f; ASFormer 2.49 f). The full-video timeline dilutes that event; a zoomed GT vs prediction strip (optionally B2 \| B3 side-by-side) would show the failure mode reviewers care about.

**Where to insert.** Immediately after `\input{tables/tab_boundary_per_transition}` and the two-sentence MAE summary in **`sec:results:boundary`** (`06_results.tex`), *before* Runtime.  
Suggested label: `fig:catch_recovery_boundary`.  
Cite in the sentence that reports catch→recovery MAE: “…(\Cref{fig:catch_recovery_boundary}).”

**Caption sketch (≤2 sentences).**  
*“Zoomed ground-truth and predicted phase labels around the catch→recovery boundary on a held-out attempt (ASFormer seed 42; optional MS-TCN panel). Vertical lines mark annotated vs predicted transition frames.”*

**Do not insert** until a cleaned PNG exists (no raw paths, labeled axes, print dpi). Prefer this over restoring the removed empty `fig_boundary_per_transition` bar chart, which duplicates `tab:boundary_per_transition`.

---

## Cross-cutting production issues

1. **Orphan floats.** Four of five Results figures lack `\Cref` before (or at) appearance — fix citations or delete floats.  
2. **150 dpi PNG.** Regenerators (`scripts/generate_asformer_figures.py`, `generate_ms_tcn_figures.py`) hard-code `dpi=150`. Target **≥300** (or PDF) for submission.  
3. **In-figure titles.** Duplicate captions; strip titles or move metadata to caption.  
4. **snake_case tick labels.** Prefer manuscript-facing names (`First pull`, `Segment F1@50`) for print.  
5. **Single-model “comparison” figure.** Do not place ASFormer-only aggregate under a B2/B3 comparison heading.

---

## Priority actions

| Priority | Action |
|----------|--------|
| P0 | Remove `fig:training_curves` from main Results |
| P0 | Remove or replace `fig:benchmark_comparison` (redundant + scale/polarity issues) |
| P1 | Cite `fig:confusion_matrix` and `fig:error_analysis` before appearance; shorten error caption |
| P1 | Regenerate kept PNGs at ≥300 dpi with axis/colorbar labels and anonymized titles |
| P2 | Add catch→recovery zoom figure in `sec:results:boundary` when asset ready |
| P2 | Optional caption trim for `fig:related_landscape` |

---

*End of figure audit.*
