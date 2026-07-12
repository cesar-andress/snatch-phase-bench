# Figure review — thesis to journal

**Thesis figures (Ilustraciones):** see thesis index p. 4.  
**Student regeneration script:** `Paper_TFM-main/scripts/generate_tfm_figures.py` → `outputs/tfm_figures/` (not present in current snapshot; script exists).

| Thesis ID | Thesis title | Approx. page | Classification | Journal target | Expected filename | Generation notes |
|-----------|--------------|--------------|----------------|----------------|-------------------|------------------|
| 4.4.1 | Esquema del flujo de datos | 14 | **Redraw** | `fig:pipeline` | `generated/fig_pipeline.pdf` | Four-layer layout: raw → annotations → keypoints → processed; remove wl_clips branding |
| 6.1.1 | Pipeline metodológico completo | 17 | **Redraw** | `fig:pipeline` or split | `generated/fig_pipeline.pdf` | Five-step pipeline; align with three-stage benchmark diagram (pose → encode → segment) |
| 6.5.1 | Representación muestra temporal | 19 | **Redraw** | `fig:window_construction` | `generated/fig_window_construction.pdf` | Use thesis schematic: 31×99 grid, center-frame marker; script `chapter6_temporal_window_representation.png` |
| 7.2.1 | Curva pérdida train/val | 23 | **Replace** | `fig:training_curves` | `generated/fig_training_curves.pdf` | Regenerate from `history.csv` after checkpoint gate; thesis figure available if LFS outputs restored |
| 7.2.2 | Curva accuracy | 23 | **Replace** | `fig:training_curves` (panel) | same | Combine loss/acc/F1 in one multi-panel figure |
| 7.2.3 | Curva macro F1 | 24 | **Replace** | `fig:training_curves` (panel) | same | Mark epoch 5 as best val per thesis |
| 7.3.1 | F1-score por fase | 25 | **Replace** | `fig:class_distribution` or results panel | `generated/fig_per_phase_f1.pdf` | **Do not use thesis numbers** until validated; structure reusable |
| 7.4.1 | Matriz de confusión | 26 | **Replace** | `fig:confusion_matrix` | `generated/fig_confusion_matrix.pdf` | From checkpoint `test_predictions.csv`; thesis CM for layout reference only |
| 7.5.1 | Precision/Recall/F1 por fase | 27 | **Discard** | — | — | Redundant with per-phase table + F1 bar; journal space |
| 5.1 | Organización del dataset | 16 | **Redraw** | `fig:dataset_overview` | `generated/fig_dataset_overview.pdf` | Thesis folder tree; upgrade to publication schematic |

---

## Additional figures (not in thesis — journal plan)

| Figure | Classification | Journal label | Notes |
|--------|----------------|---------------|-------|
| Dataset overview montage | **Create** | `fig:dataset_overview` | Needs cleared video frames |
| Split visualization | **Create** | `fig:split_visualization` | Script stub in `generate_tfm_figures.py` `plot_split_distribution` |
| Class distribution (windows) | **Create** | `fig:class_distribution` | Low risk — verified counts |
| Phase illustration timeline | **Create** | `fig:phase_illustration` | M23 ontology reconciliation |
| Benchmark comparison | **Create** | `fig:benchmark_comparison` | Phase 3 experiments |
| Boundary error per transition | **Create** | `fig:boundary_per_transition` | Phase 3 + boundary metrics |
| Error analysis overlay | **Create** | `fig:error_analysis` | Qualitative after predictions |
| Overlap schematic (stride-1) | **Create** | optional Methods | Repo adds science thesis omitted |

---

## Style guide (from thesis script)

Reuse color palette from `generate_tfm_figures.py` `PHASE_COLORS` for phase consistency across redrawn figures. Prefer vector PDF exports at 300 DPI for journal submission.

---

## Legal note

Do **not** reuse thesis figures containing identifiable athletes until video redistribution is cleared. Redraw schematics without photographic content where possible.
