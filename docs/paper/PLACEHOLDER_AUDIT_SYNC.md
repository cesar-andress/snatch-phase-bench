# Manuscript sync — placeholder production audit (2026-07-22)

Companion to [`PLACEHOLDER_AUDIT.md`](PLACEHOLDER_AUDIT.md).

The journal manuscript lives outside this Git tree at
`~/papers/snatch-phase-bench/paper/`. Production cleanup applied there:

## Completed with existing assets

- Wired `figures/generated/asformer_b3/` PNGs into:
  - `fig_confusion_matrix.tex`
  - `fig_training_curves.tex`
  - `fig_error_analysis.tex`
  - `fig_benchmark_comparison.tex`
- Moved confusion/training figure `\input`s from LSTM baseline subsection to ASFormer results.

## Removed from the build (incomplete material)

- Dataset: overview, phase illustration, split, class-distribution, window-construction figure `\input`s
- Methods: pipeline figure `\input` (replaced with one prose sentence)
- Results: boundary bar figure `\input`; empty Ablation subsection + `tab_ablation`
- `main.tex`: dropped `\input` of appendices D and E (all-`\pending` shells)
- Dangling `\Cref{fig:pipeline}` / `\Cref{fig:window_construction}` redirected or removed
- Protocol: removed stale “awaits benchmark results” sentence

## Intentionally retained `\pending` cells

- `tab_dataset_stats` native FPS/resolution (unknown metadata)
- Appendix B Zenodo DOI (release not minted)

No B1/B2/B3 numeric results were changed.
