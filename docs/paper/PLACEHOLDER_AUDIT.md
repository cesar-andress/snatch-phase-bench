# Placeholder audit — SnatchPhaseBench manuscript

**Date:** 2026-07-22  
**Scope:** Entire LaTeX tree under `~/papers/snatch-phase-bench/paper/`  
**Policy:** Complete from existing campaign assets when possible; otherwise **remove** from the build. Do not invent scientific content.

---

## Summary

| Category | Count found | Action |
|----------|-------------|--------|
| `\figplaceholder` figures in build | 11 wrappers (10 still empty in PDF) | Complete 4 with existing PNGs; remove 7 from `\input` |
| Dummy / all-`\pending` tables | Ablation + appendix D/E catalogs | Remove from main Results / drop appendices D–E from `\input` |
| `\textsc{TODO}` in body | 0 (after prior editorial pass) | — |
| Stale “await / not yet / placeholder” prose | Several | Soften or delete figure `\Cref`s |
| Placeholder citations (`\todosource`) | Macro only; unused in body | Keep macro unused |
| Missing captions | None for retained floats | — |

---

## Issues and recommendations

### A. Figures — can be completed with existing material

| File | Problem | Why problematic | Action taken |
|------|---------|-----------------|--------------|
| `fig_benchmark_comparison.tex` | Fallback `\figplaceholder` if PNG missing | Review PDF may show empty box | **Complete:** prefer `asformer_b3/aggregate_seed_stability.png` (already present) |
| `fig_confusion_matrix.tex` | Placeholder; caption still “await checkpoint” | LSTM matrix not generated; B2/B3 matrices exist | **Complete:** show ASFormer seed-42 confusion matrix; retitle as dense-baseline illustration (not LSTM) |
| `fig_training_curves.tex` | Placeholder for LSTM curves | LSTM curves absent; B3 curves exist | **Complete:** ASFormer seed-42 training curves |
| `fig_error_analysis.tex` | Placeholder qualitative | Timelines exist for B3 | **Complete:** ASFormer qualitative timeline seed-42 |

### B. Figures — cannot be completed → remove from manuscript build

| File | Problem | Why problematic | Action taken |
|------|---------|-----------------|--------------|
| `fig_dataset_overview.tex` | Needs cleared exemplar videos | Empty box; legal blocker | **Remove** `\input` from Dataset |
| `fig_phase_illustration.tex` | No exemplar graphic | Empty box | **Remove** `\input` |
| `fig_split_visualization.tex` | No plot script output in paper tree | Empty box; table already has splits | **Remove** `\input` |
| `fig_class_distribution.tex` | Plot script not shipped | Empty box; `tab_class_distribution` exists | **Remove** `\input` |
| `fig_window_construction.tex` | No TikZ asset | Empty box; notation appendix covers shapes | **Remove** `\input` + `\Cref{fig:window_construction}` |
| `fig_pipeline.tex` | No architecture export | Empty box | **Remove** `\input`; drop `\Cref{fig:pipeline}` where used |
| `fig_boundary_per_transition.tex` | No bar-chart PNG; table exists | Redundant empty float | **Remove** `\input`; keep `tab_boundary_per_transition` |

Wrapper `.tex` files may remain on disk unused; they are no longer included in `main.tex` / section inputs.

### C. Tables

| File | Problem | Why problematic | Action taken |
|------|---------|-----------------|--------------|
| `tab_ablation.tex` | Entirely `\pending`; caption said placeholder | Signals unfinished experiments | **Remove** Results ablation subsection + `\input` |
| `appendices/D_benchmark_extra.tex` | All-pending per-class table | Dummy appendix | **Remove** from `main.tex` `\input` |
| `appendices/E_error_analysis.tex` | Pending failure catalog | Dummy appendix | **Remove** from `main.tex` `\input` |
| `tab_dataset_stats.tex` FPS row `\pending` | Incomplete metadata cell | Honest unknown, not a fake figure | **Keep** (factual incompleteness, not a dummy table) |
| `tab_benchmark_comparison.tex` empty future-model rows | Visual noise | Not a placeholder graphic; scientific honesty | **Keep** for now (separate editorial issue) |
| `appendices/B_reproducibility.tex` Zenodo `\pending` | Release status | Factual | **Keep** |

### D. Prose / comments

| Location | Problem | Action |
|----------|---------|--------|
| `05_experimental_protocol.tex` “quantitative discussion awaits benchmark results” | Stale after B2/B3 | **Rewrite** to point to Results |
| Figure captions with “placeholder” / TODO | Draft tone | **Fixed** when wiring or removing |
| `macros/helpers.tex` `\todosource`, `\figplaceholder` | Infrastructure | Keep definitions; no body use of `\todosource` |
| `formatting/journal-agnostic.tex` draft watermark commented | Harmless | Leave commented |

### E. Citations / references

| Check | Result |
|-------|--------|
| `\todosource{...}` in body | None |
| `@misc{todo_*}` in bib | None |
| Undefined cites | None in prior compile of bibliography keys |

---

## Actions checklist (executed with this audit)

- [x] Wire B3 PNGs into confusion / training / error / benchmark figures  
- [x] Remove incomplete dataset/methods figure `\input`s  
- [x] Remove Results ablation subsection  
- [x] Drop appendices D and E from `main.tex`  
- [x] Fix stale Protocol sentence on autocorrelation  
- [x] Remove dangling `\Cref{fig:pipeline}` / `\Cref{fig:window_construction}`  

Scientific numbers in B1–B3 tables were **not** modified.

Manuscript edits live outside this Git tree; see [`PLACEHOLDER_AUDIT_SYNC.md`](PLACEHOLDER_AUDIT_SYNC.md).

---

*End of placeholder audit.*
