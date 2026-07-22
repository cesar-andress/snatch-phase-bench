# LaTeX clean build sync (2026-07-22)

Manuscript at `~/papers/snatch-phase-bench/paper/` now builds with:

- `pdflatex` ×3 + `bibtex`: **0** Overfull, **0** Underfull, **0** LaTeX/Package warnings, **0** BibTeX warnings
- Exit code 0; `main.pdf` 28 pages

## Fixes applied

- Robust `\repo` via `\DeclareUrlCommand` (no `\url` in moving arguments)
- Normalized `\repo{...}` arguments to literal underscores
- Compacted prior-art / seed-stability / hyperparam / reproducibility tables to text width
- Restored missing `\input{figures/fig_error_analysis}`
- Softened long `\texttt` paths in Appendix A
- `\emergencystretch=2em` in journal-agnostic layout
