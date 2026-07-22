# Table audit — SnatchPhaseBench manuscript

**Date:** 2026-07-22  
**Scope:** Tables included in the LaTeX build (`main.tex` → sections + appendices A–C + notation).  
**Excluded from scoring:** `tab_ablation.tex` and appendices D/E (removed from build in the placeholder pass).  
**Policy:** Recommend editorial/layout fixes only. **Do not change experimental numeric results.**

---

## Inventory (in build)

| Label | File | Section | Discussed in text? |
|-------|------|---------|--------------------|
| `tab:prior_art_comparison` | `tab_prior_art_comparison.tex` | Related Work | **Yes** (`\Cref` before float) |
| `tab:dataset_stats` | `tab_dataset_stats.tex` | Dataset | **Weak** — float present; no body `\Cref`; only App.~A back-ref |
| `tab:phase_taxonomy` | `tab_phase_taxonomy.tex` | Dataset | **Yes** |
| `tab:split_stats` | `tab_split_stats.tex` | Dataset | **Yes** (Protocol / Related / Dataset context) |
| `tab:class_distribution` | `tab_class_distribution.tex` | Dataset | **Yes** |
| `tab:lstm_hyperparams` | `tab_lstm_hyperparams.tex` | Methods | **Weak** — float in Methods; `\Cref` only in App.~C |
| `tab:baseline_reproduction` | `tab_baseline_reproduction.tex` | Results | **Yes** |
| `tab:baseline_perclass` | `tab_baseline_perclass.tex` | Results | **Yes** |
| `tab:benchmark_comparison` | `tab_benchmark_comparison.tex` | Results | **Yes** |
| `tab:mstcn_seed_stability` | `tab_mstcn_seed_stability.tex` | Results | **Yes** |
| `tab:asformer_seed_stability` | `tab_asformer_seed_stability.tex` | Results | **Yes** |
| `tab:segment_metrics` | `tab_segment_metrics.tex` | Results | **No `\Cref`** — F1@10 prose does not cite the table |
| `tab:mstcn_perclass_recall` | `tab_mstcn_perclass_recall.tex` | Results | **Yes** |
| `tab:asformer_perclass_recall` | `tab_asformer_perclass_recall.tex` | Results | **Yes** |
| `tab:boundary_metrics` | `tab_boundary_metrics.tex` | Results | **Delayed** — cited in Discussion, not in Results §Boundary |
| `tab:boundary_per_transition` | `tab_boundary_per_transition.tex` | Results | **Yes** |
| `tab:runtime` | `tab_runtime.tex` | Results | **Delayed** — cited in Discussion only; Results §Runtime has no `\Cref` |
| `tab:notation` | `appendices/00_notation.tex` | App. notation | **Implicit** (defines symbols; App.~referenced) |
| `tab:dataset_files` | `appendices/A_dataset.tex` | App. A | **Yes** (surrounding file-inventory prose) |
| `tab:repro_checklist` | `appendices/B_reproducibility.tex` | App. B | **Yes** (checklist section) |
| `tab:mstcn_hyperparams` | `tab_mstcn_hyperparams.tex` | App. C | **Yes** |
| `tab:asformer_hyperparams` | `tab_asformer_hyperparams.tex` | App. C | **Yes** |

**Count:** 22 tables in build.

---

## Cross-cutting issues

### 1. Duplicated metrics (same numbers, multiple tables)

| Metric | Appears in | Recommendation |
|--------|------------|----------------|
| Frame macro-F1, F1@50, Edit, MAE$_\mathrm{bnd}$ | `tab:benchmark_comparison`, seed-stability tables, `tab:segment_metrics` (subset), `tab:boundary_metrics` (MAE + Boundary F1) | Keep **one** comparison table + seed tables; slim `tab:segment_metrics` to F1@10/@25 only (unique content) **or** drop empty future rows and cite seed tables for F1@50/Edit |
| Params | `tab:benchmark_comparison`, `tab:runtime` | Drop Params from comparison; keep in runtime |
| Window Acc / Macro F1 (LSTM) | `tab:benchmark_comparison`, `tab:baseline_reproduction` | Keep LSTM detail in reproduction table; comparison may show Acc/F1 once with footnote |

**Critical labeling duplicate:** In `tab:benchmark_comparison`, columns **Frame MoF** and **Macro F1** are identical (MS-TCN 0.905 / 0.905; ASFormer 0.902 / 0.902). Campaign aggregates expose only `frame_macro_f1` (no separate MoF series). Treat Frame MoF as a **misnamed duplicate of frame macro-F1**, not a second result. **Remove the MoF column** (editorial correction of column identity; do not invent a new MoF number).

### 2. Empty / placeholder rows

| Table | Empty rows | Recommendation |
|-------|------------|----------------|
| `tab:benchmark_comparison` | B0, MS-TCN++, DiffAct, CTR-GCN→TAS | **Remove** unevaluated rows; mention future tiers in one prose sentence |
| `tab:segment_metrics` | B0, LSTM, MS-TCN++ | **Remove** empty rows; keep B2/B3 only |
| `tab:boundary_metrics` | B0 | **Remove** |
| `tab:runtime` | B0; LSTM mostly `---` | Drop B0; keep LSTM only if a real wall-clock exists, else omit |

`tab:dataset_stats` FPS/resolution `\pending` and Zenodo `\pending` in `tab:repro_checklist` are honest incompleteness — **keep** or move to Limitations (not fake rows).

### 3. Inconsistent decimal precision

| Family | Precision | Issue |
|--------|-----------|-------|
| LSTM reproduction / per-class | 4 dp (`0.9518`) | Finer than dense tables |
| Seed means (F1) | 3 dp | OK |
| Seed MAE per-seed | 3 dp (`1.746`) vs mean `1.32` (2 dp) | Align means to 2 or 3 dp consistently |
| Benchmark comparison MAE | 2 dp (`1.32`, `0.98`) | OK if seed means match |
| Per-class dense recall | 3 dp | OK |
| Boundary per transition | 2 dp | OK |

**Recommendation (formatting only):** report dense endpoints at **3 dp** for unitless scores and **2 dp** for MAE in frames across all tables; optionally round LSTM to 3 dp in the comparison table only (keep 4 dp in the reproduction gate table if the exact-match claim needs it).

### 4. Inconsistent metric order / naming

| Table | Order / names |
|-------|----------------|
| Comparison | Frame MoF, Macro F1, F1@50, Edit, MAE, Window Acc, Params |
| Seed stability | Frame macro-F1, F1@50, Edit, MAE, Boundary F1 |
| Segment | F1@10, F1@25, F1@50, Edit score, Frame macro-F1 |

**Recommendation:** Canonical order for dense models:  
`Frame macro-F1 → F1@10 → F1@25 → F1@50 → Edit → MAE$_\mathrm{bnd}$ → Boundary F1`  
Use one spelling: **Frame macro-F1** (not “Macro F1” / “Frame MoF”). Spell **Edit score** fully once per table or always “Edit”.

### 5. Inconsistent capitalization / phase naming

| Table | Style |
|-------|--------|
| `tab:class_distribution`, `tab:baseline_perclass`, `tab:boundary_per_transition` | `snake_case` / lowercase |
| `tab:mstcn_perclass_recall`, `tab:asformer_perclass_recall` | Title Case (“First pull”) |
| `tab:phase_taxonomy` | `\texttt{snake_case}` |

**Recommendation:** Match taxonomy: `\texttt{first_pull}` everywhere in numeric tables, or Title Case everywhere — pick one.

### 6. Unnecessary columns / abbreviations

| Item | Issue | Recommendation |
|------|-------|----------------|
| Frame MoF | Duplicate / undefined vs MoF literature | Remove column |
| Window Acc in comparison | Almost all `---` | LSTM footnote or drop column |
| Params in comparison | Duplicates runtime | Drop |
| “Pub.\ data”, “Repro.” | Opaque in prior-art table | Expand to “Public data”, “Reproducible” or footnote once |
| MAE$_{\mathrm{bnd}}$ (f) | “f” for frames | Prefer “(frames)” |
| `\ac{MOCAP}`, VB, MB, kp, bnd. | Dense prior-art cells | Expand on first use in caption or use a short legend |

### 7. Captions longer than necessary

| Table | Caption issue | Suggested trim |
|-------|---------------|----------------|
| `tab:prior_art_comparison` | 3 sentences + process note | 1–2 sentences; drop “at the time of writing” |
| `tab:benchmark_comparison` | 4 sentences | 2: what is shown + LSTM incomparability footnote |
| `tab:boundary_metrics` | FPS digression | One sentence; keep FPS note in Protocol only |
| `tab:mstcn_hyperparams` / `tab:asformer_hyperparams` | Long path/paper refs | One sentence + “see design doc” |
| `tab:phase_taxonomy` | Points to section already open | One sentence |

---

## Per-table notes (brief)

### Related Work / Dataset / Methods

- **`tab:prior_art_comparison`:** Valuable; very wide (`\resizebox`). Consider dropping “Relation…” into a footnote column or shortening cells. Cited correctly.
- **`tab:dataset_stats`:** Add `\Cref{tab:dataset_stats}` in Dataset overview. Drop or relocate pending FPS/legal rows if they clutter the summary.
- **`tab:phase_taxonomy`:** Keep; essential. Caption trim only.
- **`tab:split_stats` / `tab:class_distribution`:** Clean; keep. Align phase capitalization with taxonomy.
- **`tab:lstm_hyperparams`:** Cite in Methods when the LSTM is introduced (`\Cref{tab:lstm_hyperparams}`).

### Results

- **`tab:baseline_reproduction`:** Gate table — keep 4 dp if exact match is claimed. “Test windows” row repeats the same constant thrice — **drop row** (state $N$ in caption).
- **`tab:baseline_perclass`:** Keep; align naming style.
- **`tab:benchmark_comparison`:** Highest-priority cleanup (empty future rows, MoF duplicate, long caption, Params/Window Acc).
- **Seed tables:** Good primary evidence; consistent with each other. Align MAE mean precision with per-seed.
- **`tab:segment_metrics`:** Overlaps comparison/seeds; empty rows; **add `\Cref`** when stating F1@10/@25, or merge unique columns into comparison and delete this table.
- **Per-class recall tables:** Keep; consider one combined table (Phase × MS-TCN × ASFormer) to cut duplication of phase lists.
- **`tab:boundary_metrics`:** Redundant with seed-table MAE/Boundary F1 means — keep only if Discussion needs a tiny summary; else delete and cite seed tables. Cite in Results if retained.
- **`tab:boundary_per_transition`:** High value; keep. Cite already OK.
- **`tab:runtime`:** Keep B2/B3 rows; cite in Results §Runtime.

### Appendices

- **`tab:notation`:** MAE$_{\mathrm{bnd}}$ defined as **ms**, but Results report **frames** — **fix definition to frames** (or dual units). Editorial consistency; not a numeric change.
- **`tab:dataset_files`:** “verified” as a size cell is vague — replace with a concrete count or “—”.
- **`tab:repro_checklist`:** Keep; Zenodo pending OK.
- **Hyperparam tables:** Keep in appendix; captions shorter; “Source” column is useful.

---

## Discussion-coverage gaps (must fix editorially)

1. `\Cref{tab:segment_metrics}` missing in Results §Segment.  
2. `\Cref{tab:dataset_stats}` missing in Dataset.  
3. `\Cref{tab:lstm_hyperparams}` missing in Methods.  
4. `\Cref{tab:boundary_metrics}` and `\Cref{tab:runtime}` absent from their Results subsections (only Discussion).

---

## Priority actions (no numeric edits)

| Priority | Action |
|----------|--------|
| P0 | Remove **Frame MoF** column from `tab:benchmark_comparison` (duplicate of frame macro-F1) |
| P0 | Delete empty future-model / B0 rows from comparison, segment, boundary, runtime tables |
| P1 | Cite every Results/Dataset/Methods table in the local subsection before or with the float |
| P1 | Harmonize metric names, order, phase capitalization, and decimal policy |
| P2 | Deduplicate: slim `tab:segment_metrics` and/or `tab:boundary_metrics`; merge per-class recall tables |
| P2 | Shorten long captions; fix notation MAE units (frames vs ms) |
| P2 | Drop redundant “Test windows” row in `tab:baseline_reproduction` |

---

*End of table audit.*
