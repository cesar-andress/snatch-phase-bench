# Figures Plan

Legend: **Available** | **Regenerate** | **Future**

| ID | Figure | Description | Status | Source / action |
|----|--------|-------------|--------|-----------------|
| F1 | Dataset overview | Athletes, videos, annotations, keypoints | **Regenerate** | New schematic for paper |
| F2 | Methodology pipeline | Annotation → pose → windows → model | **Available** | `Paper_TFM-main/outputs/tfm_figures/chapter6_methodology_pipeline.png` |
| F3 | Temporal window construction | 31-frame window, center label | **Available** | `outputs/tfm_figures/temporal_window_construction.png` |
| F4 | Split visualization | Athlete-level train/val/test | **Regenerate** | From `athlete_split.json` + metadata |
| F5 | Class distribution | Bar chart of phase frequencies | **Available** | `chapter5_phase_distributions.png` |
| F6 | Confusion matrix | 7×7 test confusion | **Regenerate** | From validated checkpoint eval (pending) |
| F7 | Training curves | Loss, accuracy, macro-F1 | **Available** | `outputs/lstm_phases/figures/` (student repo) |
| F8 | Per-phase F1 | Bar chart per phase | **Available** | `f1_by_phase.png` |
| F9 | Benchmark comparison | Multiple models vs metrics | **Future** | After Phase 3 models |
| F10 | Ablation summary | Coordinate/window/stride ablations | **Future** | Phase 4 |
| F11 | Error analysis | Misclassified phase timelines | **Future** | Qualitative examples |
| F12 | Overlap illustration | stride-1 window overlap schematic | **Regenerate** | For methods section |
| F13 | Segment prediction timeline | GT vs predicted phases on one lift | **Future** | Segment-level eval |

## Notes

- Do not use student figures in publication without license check.
- Confusion matrix and benchmark figures must use **validated checkpoint** when available.
- Avoid athlete-identifying imagery in public figures.
