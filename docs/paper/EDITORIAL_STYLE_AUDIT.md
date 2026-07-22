# Editorial style audit — SnatchPhaseBench manuscript

**Date:** 2026-07-22  
**Role:** Managing Editor (Q1) — style, coherence, terminology  
**Science:** Assumed correct; results and conclusions not altered in substance  
**Manuscript root:** `~/papers/snatch-phase-bench/paper/`  
**Companion dictionaries:** [`TERMINOLOGY_DICTIONARY.md`](TERMINOLOGY_DICTIONARY.md), [`ACRONYM_DICTIONARY.md`](ACRONYM_DICTIONARY.md)

---

## 1. Editorial issues found

| Area | Issue |
|------|-------|
| Coherence | Abstract, Introduction, Limitations, Conclusion, and Discussion still spoke as if B2/B3 were unfinished while Results reported them |
| Voice | First-person (`we`/`We`) in Abstract, Intro, Dataset, Methods, Results, Limitations |
| Draft scaffolding | Widespread `\textsc{TODO}`, “placeholder”, “planned but not reported” |
| Emphasis | `\textbf`/`\emph`/`---` used for rhetorical stress |
| Discussion | Outline-only TODOs contradicted Results |
| Prior-art table | SnatchPhaseBench row still said “planned TAS/B0” |
| Caption bug | `tab_prior_art_comparison` temporarily lost caption closing brace during edit (fixed) |

---

## 2. Repetitions removed

- Repeated “experiments not complete / placeholders” messaging across Abstract, Intro organization, Methods opening, Protocol opening, Limitations, Conclusion.
- Duplicate “honest / seam / earn complexity” style positioning (Related Work already polished earlier).
- Results line that restated ASFormer “reduced” MAE in causal marketing tone; replaced with neutral parallel numbers.
- Redundant Discussion banner (“no performance claims at this stage”).

---

## 3. AI-style patterns removed

- First-person research narrative.
- TODO/placeholder/draft checklist language in main matter.
- Em-dash stacks and bold model-name shouting in Results.
- Formulaic “Additionally” in Protocol.
- Rhetorical/self-praise closers (earlier Related Work pass; Discussion rewritten factually).

---

## 4. Terminology corrections

| Before | After |
|--------|-------|
| Multi-model comparisons “planned / not reported” | Dense MS-TCN (B2) and ASFormer (B3) under shared protocol |
| “benchmark metrics pending” | Canonical evaluation stack + frozen dense baselines |
| “M3 training protocol” as reader-facing heading emphasis | Shared multi-seed protocol; B2 frozen |
| “reproducibility-first” (marketing) | reproducibility-oriented |
| “planned TAS/B0” in prior-art table | LSTM, MS-TCN, ASFormer |

Full dictionary: `TERMINOLOGY_DICTIONARY.md`.

---

## 5. Acronym audit

- Package definitions present for TAS, MOCAP, IMU, CV, DL, LSTM, GRU, TCN, STGCN, IoU, plus unused MAE/MoF/GCN/ML/RNN/IWF.
- Body uses `\ac` / `\acf` inconsistently for MAE/MoF (often spelled in prose).
- Recommendation: use or delete unused `\acrodef` entries at camera-ready.

See `ACRONYM_DICTIONARY.md`.

---

## 6. Figure audit

| Figure | Status | Editorial note |
|--------|--------|----------------|
| `fig:related_landscape` | TikZ OK; referenced | Keep |
| `fig:pipeline` | Placeholder wrapper | Still `\figplaceholder`; wire or drop |
| `fig:dataset_overview` | Placeholder | Same |
| `fig:phase_illustration` | Placeholder | Same |
| `fig:split_visualization` | Placeholder | Same |
| `fig:class_distribution` | Placeholder | Same |
| `fig:window_construction` | Placeholder | Same |
| `fig:confusion_matrix` | Placeholder (assets exist under `generated/`) | Wire PNGs |
| `fig:training_curves` | Placeholder | Wire PNGs |
| `fig:benchmark_comparison` | Uses ASFormer aggregate PNG when present | Caption OK |
| `fig:boundary_per_transition` | Placeholder | Wire or drop |
| `fig:error_analysis` | Placeholder | Wire or drop |

Many figures remain visually empty despite generated assets; this is a **production** residual, not a Results-number change.

---

## 7. Table audit

| Table | Status |
|-------|--------|
| Baseline / B2 / B3 metric tables | Numbers untouched |
| `tab_prior_art_comparison` | SnatchPhaseBench row updated editorially |
| `tab_ablation`, appendix D/E pending cells | Still `\pending`; captions de-placeholderized |
| Decimal precision | Left as previously frozen (3 dp / 2 dp MAE) |
| Empty leaderboard rows | Retained (honest incomplete tiers) |

---

## 8. Cross-reference audit

- Restored `\input` of baseline tables/figures after an intermediate edit risk.
- Added textual `\Cref{tab:baseline_perclass}` before that table.
- Orphan figure `\Cref`s remain for several placeholders (pre-existing production debt).
- No new BibTeX keys added in this editorial pass.

---

## 9. LaTeX audit

| Check | Status after pass |
|-------|-------------------|
| `\textsc{TODO}` in main sections | Removed / rewritten |
| Abstract contradiction | Fixed |
| First-person in main narrative | Removed from edited sections |
| Caption brace on prior-art table | Fixed |
| Appendices TODOs | Converted to factual incomplete statements |
| Figure placeholders | **Remain** |
| Ablation pending table | **Remains** |
| Overfull boxes | Not re-optimized in this pass |

---

## 10. Remaining recommendations

1. Wire `figures/generated/{ms_tcn_m3,asformer_b3}/` into confusion/training/timeline figure wrappers.
2. Drop or move empty ablation/appendix pending tables to supplementary-only builds.
3. Add `\Cref` for every retained float before `\input`.
4. Clean unused acronym definitions.
5. Recompile with protected `\repo` in captions (known production issue from prior LaTeX audit).
6. Optional: soften contribution-item `\textbf{...}` labels if the target journal dislikes bold list heads.

---

## Files touched (manuscript)

- `main.tex` (Abstract)
- `sections/01_introduction.tex`
- `sections/03_dataset.tex`
- `sections/04_methods.tex`
- `sections/05_experimental_protocol.tex`
- `sections/06_results.tex` (voice/coherence only; metrics unchanged)
- `sections/07_discussion.tex`
- `sections/08_limitations.tex`
- `sections/09_conclusion.tex`
- `tables/tab_prior_art_comparison.tex`
- `appendices/A_dataset.tex`, `B_reproducibility.tex`, `C_hyperparameters.tex`, `D_benchmark_extra.tex`, `E_error_analysis.tex`

**Not modified:** frozen numeric cells in B2/B3 result tables; Related Work (already polished); bibliography keys (no new citations).

---

*End of editorial style audit.*
