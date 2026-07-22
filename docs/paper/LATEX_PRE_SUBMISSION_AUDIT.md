# LaTeX pre-submission audit (production editor)

**Date:** 2026-07-22  
**Role:** Production editor (Q1 journal) — structural / typographic / cross-reference / artifact consistency only  
**Scope:** `~/papers/snatch-phase-bench/paper/` (LaTeX tree)  
**Build attempted:** `latexmk -pdf -f main.tex` (TeX Live 2023) → PDF written (34 pages) **with errors**  
**Software HEAD (for result tracing):** `35aa854`  
**Policy:** Report only. No scientific rewrites. No automatic fixes.

Canonical numeric sources used for tracing:

- `snatch-phase-bench/docs/benchmark/results/ms_tcn_m3/`
- `snatch-phase-bench/docs/benchmark/results/asformer_b3/`
- `snatch-phase-bench/outputs/benchmark/{ms_tcn,asformer}/seed*/eval_test.json`
- `paper/macros/notation.tex` (dataset constants)

---

## Verdict (production)

**Not ready for external scientific review.**

The PDF builds only in force mode. Captions break compilation; the manuscript still contains editorial scaffolding (`TODO`, `\pending`, figure placeholders); Abstract / Discussion / Conclusion contradict the Results body; several floats are included without textual cross-references; one primary comparison table column is not traceable to a distinct metric in the JSON schema.

---

## 1. Critical issues

| ID | Issue | Location | Why it blocks review |
|----|-------|----------|----------------------|
| C1 | **Compile errors:** `\repo{...}` → `\path{...}` used inside **table captions** (moving argument). Log: `! Undefined control sequence` / `\Url Error ->\url used in a moving argument`. | `tables/tab_mstcn_hyperparams.tex:3`, `tables/tab_asformer_hyperparams.tex:3` | Production build is unclean; cascading undefined-ref/cite warnings. |
| C2 | **Abstract contradicts Results.** Abstract states multi-model comparisons are “planned but not reported” and that `sec:results:benchmark` “remain placeholders”. | `main.tex:35–38` vs `sections/06_results.tex` (B2/B3 fully populated) | Internal inconsistency; editorial desk reject risk. |
| C3 | **Discussion / Conclusion contradict Results.** Discussion: “No performance claims… once experiments are complete.” Conclusion: “Execute multi-model benchmark…”. Results already report B2/B3. | `07_discussion.tex:3–4`, `09_conclusion.tex:3–19` vs `06_results.tex` | Incomplete camera-ready narrative structure. |
| C4 | **Limitations bullet contradicts Results.** “Benchmark scope not yet evaluated… no comparative scientific conclusions.” | `08_limitations.tex:36–37` | Same class as C2–C3. |
| C5 | **Editorial scaffolding still in body:** ≥28 `\textsc{TODO…}` macros; ≥63 `\pending` cells; ≥10 figures still emit `\figplaceholder` boxes. | Throughout sections/appendices/figures/tables | Looks like a draft, not a reviewable submission. |
| C6 | **`tab:benchmark_comparison` “Frame MoF” column not traceable.** B2/B3 rows set Frame MoF = Macro F1 = `0.905` / `0.902`. Eval JSON exposes `frame_macro_f1` only; **no separate MoF / frame-accuracy field**. | `tables/tab_benchmark_comparison.tex:15–20` | Duplicate/ambiguous metric column; cannot be traced as a distinct generated quantity. |
| C7 | **Generated PNG assets exist but most figure wrappers still show placeholders.** Assets under `figures/generated/{ms_tcn_m3,asformer_b3}/` (confusion, curves, timelines, seed stability). Only `fig_benchmark_comparison.tex` optionally includes a real PNG. | e.g. `fig_confusion_matrix.tex`, `fig_training_curves.tex`, `fig_boundary_per_transition.tex`, `fig_error_analysis.tex` | Reviewers see empty boxes while files exist on disk. |

---

## 2. High priority issues

| ID | Issue | Location |
|----|-------|----------|
| H1 | **Figures included via `\input` but never `\Cref`/`\ref`’d (orphan floats).** Unreferenced labels: `fig:benchmark_comparison`, `fig:boundary_per_transition`, `fig:class_distribution`, `fig:confusion_matrix`, `fig:dataset_overview`, `fig:phase_illustration`, `fig:split_visualization`, `fig:training_curves`. | Labels in `figures/*.tex`; inputs in §§3–6 |
| H2 | **Tables included but never cross-referenced.** Unreferenced: `tab:ablation`, `tab:baseline_perclass`, `tab:boundary_metrics`, `tab:runtime` (+ appendix tables `tab:appendix_perclass_segment`, `tab:failure_catalog`, `tab:notation`, `tab:repro_checklist`, `tab:dataset_files`). | §§6, appendices |
| H3 | **Entire appendices essentially unreferenced** from the main text (`app:reproducibility`, `app:hyperparameters`, `app:benchmark_extra`, `app:error_analysis`, …). Hyperparameter appendix is partially cited via table labels only. | `appendices/*` |
| H4 | **Ablation / appendix tables are all `\pending`.** `tab_ablation.tex` caption still says MAE in **ms** while protocol forbids ms without verified FPS. | `tables/tab_ablation.tex`; `appendices/D_*.tex`, `E_*.tex` |
| H5 | **Introduction / Methods / Protocol openings still draft-status language** while later subsections contain finished B2/B3 material. | `01_introduction.tex:57–62,75–76`; `04_methods.tex:5,87`; `05_experimental_protocol.tex:5` |
| H6 | **Stale figure TODOs** claim missing boundary metrics / checkpoint validation / scripts not implemented — superseded by B2/B3 campaigns. | e.g. `fig_boundary_per_transition.tex`, `fig_confusion_matrix.tex`, `fig_class_distribution.tex` |
| H7 | **BibTeX style `plain` + `hyperref`:** OK for draft, but journal may require numbered/author-year style; no `biblatex`. Not broken, but not production-final. | `main.tex` `\bibliographystyle{plain}` |
| H8 | **Cascading “Citation undefined” warnings in log** for `cao2022snatch` / `chen2022snatch` despite entries present in `bibliography.bib` and `main.bbl` (25/25 cites in BBL). Symptoms of C1 incomplete runs; must re-verify after caption fix. | `main.log` |
| H9 | **Placeholder cite macro** `\citep{...}` remains defined (`macros/helpers.tex:12`). Dangerous if used; currently only in macro definition. | `macros/helpers.tex` |
| H10 | **Empty / outline Discussion subsections** are still numbered headings with only TODO lines (looks like incomplete sections, not intentional omission). | `07_discussion.tex` |

---

## 3. Medium priority issues

| ID | Issue | Notes |
|----|-------|-------|
| M1 | **Terminology drift: “seven-class” vs “seven-phase” vs “eight-class logits”.** | Dataset/methods mix; eight-class = 7 phases + `unlabeled`. Needs one glossary sentence for production clarity (report only). |
| M2 | **Protocol naming: “M3 protocol” vs “B2 protocol” vs “shared B2/B3”.** | Captions: `tab_mstcn_seed_stability` says M3; ASFormer says B3; hyperparams mix M3/B2. |
| M3 | **Tier naming incomplete in Abstract** (no B1/B2/B3). Body uses B0/B1/B2/B3 unevenly. | Consistency |
| M4 | **Metric naming variants:** “frame macro-F1”, “Macro F1”, “Frame MoF”, “segment F1@50”, “F1@50”, “segmental F1”. | Same family, inconsistent surface forms |
| M5 | **Units:** boundary MAE in **frames** (correct per protocol) but ablation table header still **ms**. Runtime mixes minutes and MiB without defining conversion source in caption beyond wall-clock. | `tab_ablation`, `tab_runtime` |
| M6 | **Acronym coverage gaps:** `MAE`, `MoF`, `GCN`, `IWF` defined in `macros/acronyms.tex` but rarely/never via `\ac{}`. Model names MS-TCN / ASFormer / MediaPipe / CTR-GCN / PoseC3D not in acronym list (acceptable if spelled consistently). | |
| M7 | **~72 unused labels** (many subsection anchors never cited). Not fatal, but noisy for maintenance. | Parser count |
| M8 | **No numbered equations / algorithms** in the manuscript (none found). Methods point to repo markdown for architecture detail — production may accept; some venues require self-contained math. | Report only |
| M9 | **`tab_dataset_stats` FPS/resolution `\pending`.** | Incomplete metadata table |
| M10 | **Prior-art table still says LSTM + “planned TAS/B0”** for SnatchPhaseBench row (stale vs Results). | `tab_prior_art_comparison.tex` |
| M11 | **Overfull `\hbox`:** 11 instances (worst ~50.8 pt, also 34.3 pt). Underfull: 64. | `main.log` |
| M12 | **`fig_benchmark_comparison` caption** says it may show ASFormer *or* fall back to MS-TCN plot — ambiguous which model the reader is viewing. | `figures/fig_benchmark_comparison.tex` |
| M13 | **Bibliography notes:** `shah2026barbell` carries “Verify final publication metadata”; FineGym authorship/pages risk (not re-judged scientifically here). | `bibliography.bib` |
| M14 | **Baumann et al. named in prose without `\cite`.** | `02_related_work.tex` (production: named entity without bibliography hook) |
| M15 | **Appendix B still has Zenodo `\pending` and TODO for Phase~3 runner** despite runners existing in software. | `appendices/B_reproducibility.tex` |

---

## 4. Minor issues

| ID | Issue |
|----|-------|
| N1 | Duplicate labels: **none** found. |
| N2 | Broken `\ref`/`\Cref` targets (labels missing): **none** in static parse; log still shows undefined refs for new B2/B3 tables until a clean error-free multi-pass. |
| N3 | Unused bibliography entries: **none** (all 25 BibTeX keys cited). |
| N4 | Duplicate bibliography keys: **none**. |
| N5 | `Makefile` `clean` deletes `main.pdf`; no `latexmkrc`. |
| N6 | Draft watermark package commented out (OK). |
| N7 | Large unused-label surface on Discussion subsections is expected given TODO outline — still clutter. |
| N8 | `figures/generated/` contains seed-wise assets never wired into any `\includegraphics`. |
| N9 | Hyperlinks: ORCID `\href` in `\thanks` OK; `\repo` paths are local filesystem strings, not resolvable URLs for reviewers. |
| N10 | `plain` BST sorts alphabetically; citation order in text is not numeric sequence (expected for `plain`). |

---

## 5. Cosmetic issues

| ID | Issue |
|----|-------|
| K1 | Mixed capitalization of phase names: prose uses `\texttt{first_pull}` vs table “First pull”. |
| K2 | “RTX~4090” vs “NVIDIA RTX~4090” vs “NVIDIA GeForce RTX 4090” (hardware reports). |
| K3 | “PyTorch~2.10.0+cu128” vs “Python~3.12” formatting inconsistent across captions. |
| K4 | Em-dashes / en-dashes in TODOs and repo paths (`MS\_TCN\_M3`). |
| K5 | Leaderboard empty rows (`MS-TCN++`, `DiffAct`, `CTR-GCN`, `B0`) produce long `---` visual noise. |
| K6 | `\setstretch{1.15}` draft spacing; journals often reset. |
| K7 | TikZ related-landscape uses `orange!` fill — fine, but style differs from placeholder boxes. |

---

## 6. Result consistency (numbers)

### 6.1 Traceable and matching (OK)

Cross-check of B2/B3 **primary aggregates** and **per-seed seed-stability tables** against `test_metrics_aggregate.json` / per-seed metrics: **match at reported rounding** (2–3 decimal places).

Also matching:

- Segment F1@10 / @25 means vs `outputs/.../eval_test.json` segment macros.
- Runtime minute ranges vs `runtime_seconds/60` (B2 ≈0.46–0.84; B3 ≈8.4–15.7).
- Param counts 0.67M / 1.00M vs 670688 / 1004768.
- Peak VRAM 16 MiB / 100 MiB vs protocol freezes.
- Per-transition MAE means in `tab_boundary_per_transition` vs mean of per-seed transition MAEs.
- Per-class recalls in ASFormer/MS-TCN recall tables vs mean of `per_class_recall`.
- Dataset constants via `\const*` macros (208, 70, 49/10/11, windows, etc.).

**No B2/B3 primary-table transcription error was found.**

### 6.2 Traceable but manually typed (acceptable if process locked)

Deltas in Results prose (`+0.015`, `−0.345`, …) are derived differences, not raw JSON fields — values match `mean_B3 − mean_B2` at stated precision.

B1 window metrics in `tab_baseline_reproduction` / comparison LSTM row (`0.952`, `0.919`) round from thesis/checkpoint tables — **not** in B2/B3 JSON; trace to B1 reproduction artifacts (outside this freeze path). Treat as separately sourced.

Hyperparameter literals (`0.0005`, `λ=0.15`, dropout `0.5`/`0.3`) come from design docs/configs, not result JSON — expected.

### 6.3 Not traceable / problematic

| Number / cell | Location | Flag |
|---------------|----------|------|
| **Frame MoF** = Macro F1 | `tab_benchmark_comparison` | **No distinct MoF in eval JSON** (C6) |
| All `\pending` cells | Ablation, appendix D/E, dataset FPS | No source by design (placeholders) |
| Placeholder figure interiors | Most `fig_*.tex` | No numeric claim, but non-final art |

---

## 7. Cross-reference & bibliography inventory

| Check | Result |
|-------|--------|
| Duplicate labels | 0 |
| Missing label for `\ref`/`\Cref` (static) | 0 |
| Undefined cites vs `.bib` keys | 0 (keys exist) |
| Unused `.bib` entries | 0 |
| `\todosource` / `\citep{...}` in body | Macro only |
| Equations | None |
| Algorithms | None |
| Compile with errors | Yes (C1) |
| PDF pages | 34 |

---

## 8. Consistency checklist (names)

| Concept | Status |
|---------|--------|
| Dataset name `SnatchPhaseBench` | Consistent |
| Models MS-TCN / ASFormer / LSTM | Consistent spelling |
| Tiers B0/B1/B2/B3 | Present in Results/Methods; **missing/contradicted in Abstract/Conclusion** |
| Ontology seven-class / `seven_phase_v1` | Mixed surface forms (M1) |
| Metrics F1@τ / edit / boundary MAE (frames) | Mostly consistent; MoF column issue (C6); ablation ms (M5) |
| Acronyms via `\ac{}` | Partial coverage (M6) |

---

## 9. Production recommendations

**Do not treat as scientific advice — production sequencing only.**

1. **Unblock compile (C1):** protect `\repo` in captions (`\protect\repo{...}` or plain `\texttt{...}` / `\url` with `\usepackage{xurl}` + `\Path` safe caption pattern). Clean `latexmk -C && latexmk -pdf` until **zero** `!` errors and zero undefined refs/cites.
2. **Remove or quarantine all `\textsc{TODO}` / `\pending` / `\figplaceholder` from the review PDF** (move unfinished appendices out of `\input` or mark Supplementary explicitly).
3. **Synchronize Abstract, Intro contribution bullets, Methods/Protocol openings, Limitations, Discussion banner, Conclusion** with the existing Results floats (editorial consistency only).
4. **Wire or drop orphan floats:** every `\input{figures/...}` / `\input{tables/...}` must be mentioned with `\Cref{...}` or removed from the build.
5. **Point figure wrappers at existing `figures/generated/**` assets** or delete unused PNGs from the submission bundle.
6. **Resolve Frame MoF column:** replace with a JSON-backed metric or remove column (C6).
7. **Fix ablation units** (ms → frames or remove table from build).
8. **Add short in-manuscript glossary** for seven-class vs eight-logit and B-tier names (one paragraph / footnote — production clarity).
9. **Re-run BibTeX after clean compile;** confirm no “Citation undefined” remains for `cao2022snatch` / `chen2022snatch`.
10. **Reduce overfull boxes** >20 pt before publisher class switch.
11. **Decide bibliography style** with target journal (replace `plain` when template known).
12. **Do not regenerate or edit frozen B2/B3 numeric artifacts** for this cleanup; only LaTeX wiring and status language.

---

## 10. Suggested production gate

| Gate | Pass? |
|------|------:|
| Clean compile (no `!`) | **No** |
| Zero undefined refs/cites after clean multi-pass | **No** (blocked by C1) |
| Zero TODO/pending/placeholder in main matter | **No** |
| Abstract ↔ Results consistent | **No** |
| All floats cross-referenced | **No** |
| All reported primary metrics traceable | **Partial** (MoF column fails) |
| Ready for external scientific reviewers | **No** |

---

*End of production audit. No files in the LaTeX tree were modified.*
