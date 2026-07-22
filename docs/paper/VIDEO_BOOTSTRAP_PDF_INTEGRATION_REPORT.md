# Video metadata + bootstrap PDF integration report

**Date:** 2026-07-22  
**Manuscript:** `~/papers/snatch-phase-bench/paper/main.pdf`  
**Evidence (not recomputed):**
- `docs/dataset/VIDEO_METADATA_AUDIT.md`
- `docs/paper/BOOTSTRAP_ANALYSIS.md`
- `analysis/bootstrap/bootstrap_summaries.json`

---

## 1. Files modified

### Manuscript (`../paper/`)
| File | Role |
|------|------|
| `main.tex` | Abstract wording; include appendix D |
| `sections/03_dataset.tex` | ffprobe/CFR audit paragraph |
| `sections/05_experimental_protocol.tex` | Paired bootstrap method (same athlete indices) |
| `sections/06_results.tex` | Bootstrap narrative + table; pointer to appendix figure |
| `sections/07_discussion.tex` | Interpretive reading; FPS construct threat revised |
| `sections/08_limitations.tex` | Exact 25 fps; bootstrap limits; no fabricated IAA |
| `sections/09_conclusion.tex` | Evidence-proportional wrap-up |
| `tables/tab_bootstrap_b3_minus_b2.tex` | Compact Δ table with Interpretation column |
| `figures/fig_bootstrap_forest.tex` | Appendix float for forest plot |
| `figures/generated/bootstrap/bootstrap_diff_forest.pdf` | Regenerated vector figure from stored CIs |
| `appendices/D_benchmark_extra.tex` | Host forest plot; note histograms stay in repo |

### Software repo (`snatch-phase-bench/`)
| File | Role |
|------|------|
| `scripts/run_athlete_paired_bootstrap.py` | Two-panel publication forest generator |
| `analysis/bootstrap/bootstrap_diff_forest.png` | Regenerated (from stored summaries; no new bootstrap draws) |
| `docs/paper/VIDEO_BOOTSTRAP_PDF_INTEGRATION_REPORT.md` | This report |

---

## 2. Manuscript sections updated

- Abstract (conservative bootstrap sentence)
- Dataset / video collection
- Experimental protocol / statistical testing
- Results / athlete-paired bootstrap
- Discussion / interpretation + threats
- Limitations
- Conclusion
- Appendix D (forest plot)

---

## 3. Exact table added

`tab:bootstrap_b3_minus_b2` — columns: Metric | Mean Δ | 95% CI | Interpretation

| Metric | Mean Δ | 95% CI | Interpretation |
|--------|--------|--------|----------------|
| Frame macro-F1 | +0.000 | [−0.015, +0.013] | No clear separation |
| Segment F1@10 | +0.004 | [−0.007, +0.016] | No clear separation |
| Segment F1@25 | −0.010 | [−0.023, +0.003] | No clear separation |
| Segment F1@50 | +0.015 | [−0.004, +0.032] | No clear separation |
| Boundary MAE | −0.344 f / −13.8 ms | [−0.448, −0.242] f | Consistent B3 advantage in this cohort |

Definition: $Δ=\mathrm{B3}-\mathrm{B2}$. Negative MAE favors B3. No p-values or asterisks.

---

## 4. Forest plot placement

**Decision: appendix (supplement), not main Results.**

| Option | Choice |
|--------|--------|
| Main paper | Compact bootstrap **table** only |
| Appendix D | Two-panel **forest PDF** (`fig:bootstrap_forest`) |
| Repository only | Histogram distributions (`bootstrap_diff_distributions.*`) |

**Justification:** Main Results already carries many campaign tables; the compact Δ table with an Interpretation column is sufficient for the narrative. The forest plot uses separate axes for F1 vs MAE (different scales) and adds visual CI support without crowding the main section. Histograms remain repository-only.

Main text references `\Cref{fig:bootstrap_forest}` after stating the numerical interpretation.

---

## 5. Confirmations

| Item | Status |
|------|--------|
| 1 frame = 40 ms used (25 fps CFR) | Yes (Dataset, Protocol, Results, table, figure twin axis) |
| Experiments recomputed | **No** |
| Predictions modified | **No** |
| Numbers fabricated | **No** (from `bootstrap_summaries.json` / audit doc) |
| Forest regenerated from stored CIs only | Yes |
| IAA results integrated | **No** (labels unavailable) |

---

## 6. Remaining limitations (stated in manuscript)

- $n=11$ fixed test athletes
- Seed averaging precedes athlete bootstrap; training runs not separately bootstrapped
- No model retraining during bootstrap; no LOAO
- Single annotator; IAA not measured
- MediaPipe pose error unquantified; camera/demographics incomplete
- External corpora may use other FPS

---

## 7. PDF compilation status

| Check | Result |
|-------|--------|
| `pdflatex` + `bibtex` + `pdflatex`×2 | **Success** (`EXIT:0`) |
| Output | `paper/main.pdf` |
| `fig:bootstrap_forest` / `tab:bootstrap_b3_minus_b2` resolved | Yes |
| Overfull/Underfull from new floats | None observed in final log |
| Undefined references (final) | None for new labels |

Appendix D also still contains legacy `\pending` segment-recall placeholders from earlier drafting; they are unrelated to this integration and do not block compilation.

---

## 8. Go / No-Go (this integration only)

**Go** for integrating video metadata + athlete-paired bootstrap into the compiled manuscript.

Conservative language, audited timing, and bootstrap CIs are aligned with repository artifacts. Do **not** treat architecture ranking as the paper’s primary claim. Hold IAA until second-annotator labels exist.

---

*End of report.*
