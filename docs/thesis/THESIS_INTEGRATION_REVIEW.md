# Thesis integration review (second pass)

**Review date:** 2026-07-13  
**Thesis source (read-only):** `~/Descargas/BMEM_49028285-54566-260531200716 - TFM_-_IA_para_la_deteccion_del_gesto_tecnico_de_la_arrancada_en_halterofilia (1).pdf`  
**Note:** The path referenced in Phase 1 (`~/papers/...pdf`) is no longer present; content was re-read from `~/Descargas/`.

**Purpose:** Identify what from the MSc thesis should transfer into the **journal manuscript** and SnatchPhaseBench documentation—without rewriting the thesis.

**Companion files (manuscript folder, outside Git):**

- [`../paper/MISSING_FROM_THESIS.md`](../paper/MISSING_FROM_THESIS.md)
- [`../paper/FIGURE_REVIEW.md`](../paper/FIGURE_REVIEW.md)
- [`TABLE_REVIEW.md`](TABLE_REVIEW.md)

---

## Executive summary

The thesis is a **functional MSc proof-of-concept** (MediaPipe + sliding-window LSTM) with a **substantial custom dataset** and honest limitations. It is **not** structured as a benchmark paper. For SnatchPhaseBench:

- **Keep:** dataset construction narrative, athlete-level split rationale, preprocessing details, per-phase error analysis, confusion patterns, future-work items aligned with benchmark roadmap.
- **Rewrite:** contribution framing (LSTM-centric → benchmark-centric), state of the art (verify citations; align with literature foundation), results claims (checkpoint-gated), applied coaching claims (tone down until segment metrics exist).
- **Discard:** educational TFM boilerplate, placeholder abstract/resumen, `wl_clips/` path references, objective-compliance tables as paper content, thesis-only “system works” conclusions without benchmark protocol.

---

## Task 1 — Scientific extraction (classified)

| Element | Thesis location | Classification | Notes |
|---------|-----------------|----------------|-------|
| Motivation: expert annotation limits, snatch complexity | Cap. 1–2 | **Should be rewritten** | Core ideas in manuscript intro; remove MSc framing |
| Gap: limited auto phase segmentation in weightlifting | Cap. 4.5 | **Already incorporated** (partial) | Manuscript Related Work outline; needs verified citations |
| Dataset: 208 videos, 70 athletes | Cap. 5, Table 4.4.1 | **Already incorporated** | Verified in repo + manuscript tables |
| Filename encoding (weight class, attempt, ok/fail) | Cap. 5 | **Should be incorporated** | Missing from `dataset.md`; needed for metadata table |
| Olympic video search/download workflow | Cap. 3, 5 | **Should be incorporated** | Legal/provenance section; not verified in repo |
| Clip cutting / temporal delimitation | Cap. 3, 5 | **Should be incorporated** | `cutting_clips.py` exists in student repo; not documented canonically |
| Phase taxonomy (7 + unlabeled) | Cap. 5–6 | **Already incorporated** | Ontology reconciliation vs 5-phase literature still open |
| Transition phase = short, ambiguous boundaries | Cap. 5, 7.3 | **Already incorporated** | Limitations + class distribution |
| MediaPipe extraction settings | Cap. 6.3 | **Partially incorporated** | Skip-if-exists, master-CSV filter; model version pending |
| Interpolation + forward/back fill | Cap. 6.4 | **Already incorporated** | Frozen pipeline verified |
| Window 31, stride 1, center label, drop unlabeled | Cap. 6.4 | **Already incorporated** | Verified exact rebuild |
| 99 features (x,y,z × 33) | Cap. 6.5 | **Already incorporated** | |
| Athlete-level split rationale | Cap. 6.6 | **Already incorporated** | Manuscript + split test |
| Per-split phase counts (Table 6.6.2) | Cap. 6.6 | **Should be incorporated** | Only aggregate split in manuscript; useful for imbalance discussion |
| LSTM hyperparameters | Cap. 6.7, Table 6.7.1 | **Already incorporated** | `tab:lstm_hyperparams` |
| Train-only standardization | Cap. 6.8 | **Already incorporated** | |
| Class-weighted CE, macro-F1 early stop | Cap. 6.8 | **Already incorporated** | |
| Window-level metrics only | Cap. 6.9 | **Already incorporated** | Benchmark plan extends to segment/boundary |
| Limitations: own dataset, manual annotation, no formal tests | Cap. 6.10 | **Already incorporated** | Manuscript limitations |
| Global metrics 0.9518 / 0.9186 | Cap. 7.1 | **Should be rewritten** | Placeholder only until checkpoint validated |
| Best val epoch 5, macro-F1 0.8991 | Cap. 7.2 | **Should be incorporated** | Training dynamics; not in manuscript yet |
| Per-phase F1 (transition 0.822, catch 0.882) | Cap. 7.3, Table 7.3.1 | **Should be incorporated** | After checkpoint gate; informs discussion |
| Confusion: adjacent-phase errors | Cap. 7.4 | **Should be rewritten** | Discussion outline exists; needs validated CM |
| Applied coaching viability claims | Cap. 7.5–8 | **Should be discarded** (for now) | Too strong without segment/boundary evidence |
| Future work: IAA, biomechanical features, GRU/TCN/Transformer | Cap. 9 | **Already incorporated** | Benchmark plan + PAPER_TODO |
| Segment labels as complementary annotation | Cap. 5 | **Should be incorporated** | Segment eval not in thesis results; key for benchmark |
| No overlap/stride discussion | — (absent) | **Should be incorporated** | Repo autocorrelation analysis supersedes thesis |
| Rule-based / knee-angle baseline | — (absent) | **Should be incorporated** | Literature foundation requirement |
| Resumen/Abstract placeholders | Front matter | **Discard** | Incomplete thesis front matter |

---

## Task 2 — Hidden contributions (not yet in repo/manuscript)

| Hidden item | Thesis evidence | Where it should live |
|-------------|-----------------|----------------------|
| **Video filename schema** (modality, weight, athlete, attempt, ok/fail, id) | Cap. 5 | `docs/dataset/dataset.md`, paper §Dataset |
| **Dual annotation export** (frame + segment, per-video CSVs + masters) | Cap. 5–6 | `dataset.md`, appendix A |
| **Interactive annotation UX** (OpenCV, frame navigation) | Cap. 6.2 | `docs/dataset/ANNOTATION_PROTOCOL.md` (future) |
| **`annotate_phases_final2.py` vs `annotate_phases.py`** naming drift | Cap. 6.2 | Student Q&A; provenance doc |
| **Pose extraction idempotency** (skip processed videos) | Cap. 6.3 | `docs/reproduction/code_provenance.md` |
| **Restrict extraction to master annotation list** | Cap. 6.3 | Reproducibility appendix |
| **Phase color palette** for figures | `generate_tfm_figures.py` | Figure regeneration style guide |
| **Best epoch = 5** (not 13) with early stopping | Cap. 7.2, `history.csv` | Results training curves caption |
| **Per-split class imbalance table** | Cap. 6.6 Table 2 | Paper appendix / imbalance discussion |
| **Segment master: 1,766 segments** | Cap. 5 (typo 1.766 in text = 1,766) | Dataset stats |
| **37,125 frame labels** (thesis) vs **35,825** (audit) | Cap. 5 vs audit | **Inconsistency to resolve** with student |
| **Barbell trajectory literature positioning** | Cap. 4.3 (Balsalobre, Nagao) | Related Work § weightlifting CV |
| **Explicit “pipeline reproducible” post-submission packaging** | Student README | Canonical repro docs (done) |

---

## Task 3–6

See dedicated files:

- [`../paper/MISSING_FROM_THESIS.md`](../paper/MISSING_FROM_THESIS.md)
- [`../paper/FIGURE_REVIEW.md`](../paper/FIGURE_REVIEW.md)
- [`TABLE_REVIEW.md`](TABLE_REVIEW.md)

---

## Task 7 — Reviewer perspective by thesis chapter

| Chapter | Valuable | Weak | Missing | Strengthen for journal |
|---------|----------|------|---------|------------------------|
| **1 Intro** | Snatch complexity, segmentation need | Generic AI sport intro | Benchmark positioning, reproducibility | Reframe as benchmark gap |
| **2 Motivation** | Coach variability, markerless access | MSc program paragraph | Legal/video source | Coaching claims → optional future work |
| **3 Objectives** | Dataset creation steps checklist | LSTM-as-goal framing | B0 baseline, segment metrics | Map objectives to benchmark tiers |
| **4 Related work** | Zhao 3-level DL, Tharatipyakul gap, WL barbell refs | Unverified citations, long tutorials | TAS benchmarks, OpenCap/Theia3D validity | Replace with verified bib + literature foundation |
| **5 Dataset** | Rich construction narrative, stats | `wl_clips/` paths, frame count discrepancy | FPS, camera, license, IAA | Metadata table + provenance |
| **6 Methods** | Clear pipeline, hyperparams, split logic | Window-classification framed as full segmentation | Overlap analysis, segment eval | Three-stage pipeline + B0 |
| **7 Results** | Per-phase analysis, confusion interpretation | Strong extrapolation, no checkpoint uncertainty | Segment/boundary metrics, stats tests | Placeholders until validated |
| **8 Conclusions** | Limitations list | Repeats results as definitive | Benchmark contribution | Do not copy to journal conclusion |
| **9 Future work** | IAA, architectures, biomech features | — | Clean & jerk as dataset expansion | Already in benchmark plan |

---

## Task 8 — Cross-reference inconsistencies

| Topic | Thesis | Repository / manuscript | Action |
|-------|--------|-------------------------|--------|
| Frame label rows | 37,125 | 35,825 (audit/rebuild) | Ask student; fix one source |
| Segment count | 1,766 | 856 per-video files (audit) | Clarify master vs per-video |
| Paths | `wl_clips/` | `Paper_TFM-main/` | Never cite wl_clips in paper |
| Annotation script | `annotate_phases_final2.py` | `annotate_phases.py` | Document canonical script |
| Contribution | LSTM system | Benchmark + dataset | Manuscript already reframing |
| Evaluation | Window accuracy | Segment + boundary planned | Benchmark plan |
| Phase count narrative | 3 pulls vs 7 labels | 7 classes | Clarify biomechanics text vs taxonomy |
| Results | 0.9518 definitive | Checkpoint not validated | Gate per FROZEN_BASELINE |
| Related citations | Pietraszewski 2025, etc. | Placeholders only | Verify before use |
| tfm_figures | Referenced in thesis/repo script | Not in current snapshot outputs | Regenerate from script or placeholders |

---

## Task 9 — Prioritized action checklist

| Priority | Action | Impact | Effort |
|----------|--------|--------|--------|
| P0 | Resolve frame-label count discrepancy (37,125 vs 35,825) | Very High | Low |
| P0 | Document video provenance + filename schema from Cap. 5 | Very High | Medium |
| P0 | Gate thesis metrics behind checkpoint validation | Very High | Low (process) |
| P1 | Add per-split phase table from thesis Table 6.6.2 to appendix | High | Low |
| P1 | Transfer annotation protocol details (Cap. 6.2) to dataset docs | High | Medium |
| P1 | Incorporate best-epoch / training dynamics from Cap. 7.2 | High | Low |
| P1 | Map thesis confusion analysis (Cap. 7.4) to discussion template post-CM | High | Medium |
| P2 | Redraw pipeline/window figures (thesis Ilustraciones 6.1.1, 6.5.1) | High | Medium |
| P2 | Extract barbell-CV related work bullets from Cap. 4.3 with verified cites | Medium | Medium |
| P2 | Document clip cutting workflow (`cutting_clips.py`) | Medium | Low |
| P3 | Mine Cap. 9 for benchmark ablation list (biomech features) | Medium | Low |
| P3 | Discard/copy-edit MSc motivation paragraphs | Low | Low |

---

## Task 10 — Final recommendation

**If the thesis disappeared tomorrow, we would regret not having transferred:**

1. **Dataset construction provenance** — Olympic video acquisition, clip cutting, filename semantics, annotation tool behavior, dual frame/segment exports (Cap. 3, 5, 6.2).
2. **Operational phase definitions and annotation caveats** — especially transition/catch ambiguity and `unlabeled` handling (Cap. 5–6, 7.3).
3. **Per-split class distribution table** — train/val/test phase counts (Cap. 6.6 Table 2); explains imbalance better than global counts alone.
4. **Training dynamics metadata** — best validation epoch 5, early stopping behavior, link to `history.csv` (Cap. 7.2).
5. **Qualitative error taxonomy** — adjacent-phase confusion pairs (Cap. 7.4); directly feeds benchmark discussion once segment metrics exist.
6. **Thesis future-work list** — IAA, biomechanical derived features, architecture comparison, robustness tests (Cap. 9); already aligned with benchmark plan but should be traceable to thesis.
7. **Explicit limitations the student already admitted** — no public benchmark, manual annotation, no industrialized testing (Cap. 6.10); strengthens journal limitations without new claims.

**We would NOT regret losing:** placeholder abstracts, MSc objective-compliance tables, `wl_clips` paths, definitive coaching claims, or the thesis conclusion prose (journal conclusion must wait for benchmark evidence).

---

## Git vs manuscript locations

| File | Location | In Git? |
|------|----------|---------|
| This review | `docs/thesis/THESIS_INTEGRATION_REVIEW.md` | Yes |
| Missing content tracker | `paper/MISSING_FROM_THESIS.md` | No (local paper/) |
| Figure review | `paper/FIGURE_REVIEW.md` | No |
| Table review | `docs/thesis/TABLE_REVIEW.md` | Yes |

Canonical copies of paper trackers are mirrored under `docs/thesis/` for version control where noted.
