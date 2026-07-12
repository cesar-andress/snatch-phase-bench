# Living Manuscript — Writing Status

**Manuscript path:** `paper/main.tex`  
**Last updated:** 2026-07-13  
**Policy:** No unverified quantitative claims in narrative text; results tables remain placeholders until experiments complete.

## Section completion

| Section | Completion % | Evidence status | Blocking dependencies |
|---------|-------------:|-----------------|------------------------|
| Abstract | 75 | Verified (infrastructure); metrics withheld | Checkpoint validation; benchmark results |
| 01 Introduction | 90 | Verified | Bibliography for motivation citations |
| 02 Related Work | 35 | Outline only; no verified citations yet | Literature review + `bibliography.bib` entries |
| 03 Dataset | 85 | Verified counts, splits, preprocessing | Video metadata; legal release; phase definitions |
| 04 Methods | 80 | Verified baseline pipeline | Benchmark model implementations (Phase 3) |
| 05 Experimental Protocol | 75 | Verified baseline protocol | Statistical testing plan; GPU runtime logs |
| 06 Results | 15 | Placeholders only | Checkpoint eval; benchmark; ablations |
| 07 Discussion | 10 | Outline only | All results tables + citations |
| 08 Limitations | 70 | Verified audit/reproduction limits | Optional pose-error quantification |
| 09 Conclusion | 5 | Outline only | Discussion + benchmark completion |

## Figures

| Figure | Label | Status | Blocking dependencies |
|--------|-------|--------|------------------------|
| Pipeline | `fig:pipeline` | Placeholder | Regenerate from codebase diagram |
| Window construction | `fig:window_construction` | Placeholder | Illustration task |
| Dataset overview | `fig:dataset_overview` | Future work | Cleared exemplar videos |
| Split visualization | `fig:split_visualization` | Future work | Publication-ready split chart |
| Class distribution | `fig:class_distribution` | Needs regeneration | Auto-generate from verified counts |
| Confusion matrix | `fig:confusion_matrix` | Future work | Checkpoint validation |
| Training curves | `fig:training_curves` | Needs regeneration | `history.csv` or retrain logs |
| Benchmark comparison | `fig:benchmark_comparison` | Future work | Phase 3 experiments |
| Error analysis | `fig:error_analysis` | Future work | Validated predictions |

See also `docs/figures_plan.md` for the project-wide figure tracker.

## Tables

| Table | Label | Status | Blocking dependencies |
|-------|-------|--------|------------------------|
| Phase taxonomy | `tab:phase_taxonomy` | Written (names only) | Biomechanical definitions |
| Split statistics | `tab:split_stats` | Verified | None |
| Class distribution | `tab:class_distribution` | Verified | None |
| Dataset statistics | `tab:dataset_stats` | Partial | FPS, resolution, release |
| LSTM hyperparameters | `tab:lstm_hyperparams` | Verified | None |
| Baseline reproduction | `tab:baseline_reproduction` | Shell only | `best_model.pt` validation |
| Per-class baseline | `tab:baseline_perclass` | Shell only | Checkpoint validation |
| Benchmark comparison | `tab:benchmark_comparison` | Shell only | Phase 3 experiments |
| Segment metrics | `tab:segment_metrics` | Shell only | Frame/segment inference |
| Ablation | `tab:ablation` | Shell only | Ablation experiments |
| Runtime | `tab:runtime` | Shell only | Standardized hardware runs |

See also `docs/tables_plan.md`.

## Bibliography

| Category | Verified entries | Placeholder entries |
|----------|------------------:|--------------------:|
| Weightlifting biomechanics | 0 | 1 |
| Markerless pose | 0 | 1 |
| Temporal segmentation | 0 | 1 |
| Sports analytics | 0 | 1 |
| Motion capture | 0 | 1 |
| Weightlifting CV | 0 | 1 |
| SnatchPhaseBench repository | 1 | 0 |

**Rule:** Replace `@misc{todo_*}` entries with verified `@article` / `@inproceedings` records before submission.

## Overall manuscript completion

| Metric | Estimate |
|--------|----------|
| **Narrative prose (verified content only)** | ~55% |
| **Structure + placeholders** | ~85% |
| **Submission-ready** | ~20% |

## Next writing actions

1. Obtain and validate `best_model.pt`; populate `tab:baseline_reproduction` and `fig:confusion_matrix`.
2. Add verified citations to Related Work (remove `\todosource{...}` macros).
3. Confirm video metadata and legal status for Dataset subsection.
4. Run Phase 3 benchmark experiments; populate `tab:benchmark_comparison` and Discussion.
5. Generate `fig:class_distribution` from verified counts (low risk, no new experiments).

## Synchronization with software

| Software artifact | Manuscript anchor |
|-------------------|-------------------|
| `configs/baseline_lstm.yaml` | `tab:lstm_hyperparams`, `sec:protocol:training` |
| `docs/dataset/dataset.md` | `sec:dataset` |
| `docs/evaluation_metrics.md` | `sec:protocol:metrics` |
| `docs/reproduction/REPRODUCTION_SUMMARY.md` | `sec:results:baseline`, `sec:limitations` |
| `docs/FROZEN_BASELINE.md` | Methods/preprocessing freeze policy |

Future benchmark merges should update `tab:benchmark_comparison` and `fig:benchmark_comparison` without restructuring sections.
