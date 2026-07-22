# Final internal review — SnatchPhaseBench

**Date:** 2026-07-22  
**Reviewer role:** Senior co-author (final internal read)  
**Manuscript:** `~/papers/snatch-phase-bench/paper/` (post–Related Work + editorial coherence pass)  
**Mode:** Identify issues only; no rewrite in this document  

---

## 1. Overall impression (≤1 page)

The paper has a clear, defensible spine: a reproducibility-oriented snatch phase benchmark on fixed MediaPipe pose, with athlete-disjoint splits, a verified historical LSTM checkpoint, and two frozen dense segmenters (MS-TCN, ASFormer) under a shared multi-seed protocol. Related Work now answers “why a new benchmark?” without overselling architecture. Results tables for B2/B3 look coherent and carefully caveated against window-level LSTM metrics.

What still stops a skeptical Reviewer #2 is not the absence of ideas, but the **gap between a mature software artifact and a still half-visual manuscript**. Several figures remain literal placeholders while campaign PNGs already exist on disk. The main comparison table mixes incomparable columns (Frame MoF duplicated with Macro F1; empty B0/MS-TCN++/DiffAct rows). Ablation is an empty shell. There is no inter-annotator agreement, no FPS for boundary-ms, and no athlete-level significance test—yet Results/Discussion report B3–B2 deltas that invite ranking language. Public video release is still pending, which weakens any “benchmark” claim aimed at a Q1 venue that expects downloadable evaluation.

Read as a co-author: the scientific story is almost ready; the **submission package** is not. One focused day of production fixes (figures, leaderboard cleanup, soften ranking, one qualitative boundary figure) would raise confidence more than another literature paragraph.

---

## 2. Top 10 issues to address before submission

| # | Issue | Why a reviewer pauses | Suggested direction (not rewriting here) |
|---|--------|----------------------|------------------------------------------|
| 1 | **Placeholder figures in the PDF** (confusion matrix, training curves, boundary-per-transition, error analysis, several dataset figures) | Looks unfinished; undermines trust after claiming verified campaigns | Wire existing `figures/generated/**` or remove floats from the build |
| 2 | **`tab:benchmark_comparison` readability** — Frame MoF = Macro F1; many `---` rows; LSTM mixed with dense metrics | “Compared to what?” / “Is MoF real?” | Drop MoF or define it; shrink to B1/B2/B3 (+ optional empty footnote for future tiers) |
| 3 | **Empty ablation subsection** | Signals incomplete experiments | Move to appendix “not reported” or delete section |
| 4 | **No IAA / single annotator** | Gold-standard quality challenge | Already in Limitations; strengthen Discussion with what can/cannot be claimed |
| 5 | **B2 vs B3 deltas without athlete-level uncertainty** | “Is +0.015 F1@50 meaningful?” | Soften ranking language further or add bootstrap/LOAO note as explicit non-claim |
| 6 | **Boundary MAE only in frames; FPS unknown** | Biomechanics readers want ms / real time | Keep frames; state coaching interpretation limits more bluntly in Discussion |
| 7 | **`catch→recovery` is the story—but qualitative evidence is a placeholder** | Hardest result lacks a readable figure | One timeline or overlay example would carry more weight than another table |
| 8 | **B0 empty while story historically promised a kinematic heuristic** | Incomplete leaderboard vs motivation | Either implement minimal B0 or stop listing it in the main comparison table |
| 9 | **Public data still Pending** | “How do I reproduce?” | Absolute paths / snapshot dependency must be crystal-clear in reproducibility appendix |
| 10 | **Intro contribution #6 is “pending legal review”** | Sounds like an unfinished checklist item | Reframe as a limitation, not a contribution |

---

## 3. Minor improvements

- Confusion-matrix figure caption still says “Do not populate until checkpoint evaluation succeeds” — stale after EXP-01 passed.
- Results § qualitative ends with repo paths; fine for artifact papers, odd for some journals—consider footnote.
- Discussion “Practical implications” is thin; either expand one concrete coaching use of boundary MAE or shorten to two sentences.
- Seven-class vs eight-logit (unlabeled) still easy to miss on first read; one Methods sentence is enough for most reviewers.
- `tab_prior_art` is dense/small; risk of “table too hard to read.”
- Paper organization subsection is optional for many venues; not harmful.
- Abstract still does not state headline B2/B3 numbers (optional; some venues prefer no numbers in abstract).

---

## 4. Possible reviewer criticisms

1. “This is a software/reproducibility paper with two off-the-shelf segmenters—where is the scientific insight beyond releasing a dataset?”
2. “Without IAA, phase boundaries are not a reliable gold standard.”
3. “Empty rows and placeholder figures indicate the manuscript was submitted mid-pipeline.”
4. “ASFormer looks better on F1@50/MAE, but with n=3 seeds and one split this is not a robust ranking.”
5. “Why include LSTM in the same table if metrics are incomparable?”
6. “Boundary error in frames without FPS is not biomechanically interpretable.”
7. “How can the community adopt the benchmark if raw video/keypoints cannot be redistributed?”
8. “Ontology diverges from five-phase knee standards—results are not comparable to Thiele/Cao.”
9. “No ablation on pose quality, windowing, or encoders—conclusions about architecture are weak.”
10. “Related Work claims a unique seam; prove no closer unpublished or niche dataset exists.”

---

## 5. Quality questions (honest)

| Question | Answer |
|----------|--------|
| Weakest section | **Results visuals + Ablation** (content strong; presentation incomplete). Among prose: **Discussion/practice** is still thin relative to Results density. |
| Weakest paragraph | Results qualitative closing that points to repo markdown instead of interpreting one failure mode with evidence in-figure. |
| Weakest figure | Any still-`figplaceholder` float that appears in §Results (especially confusion matrix / error analysis). |
| Weakest table | `tab:benchmark_comparison` (MoF duplication + empty tiers). |
| Least convincing claim | Implicit ranking of ASFormer over MS-TCN from seed means without athlete-level uncertainty. |
| Hardest explanation | Why eight-class logits / unlabeled coexist with “seven-class” evaluation—easy to confuse. |
| Result needing more discussion | **`catch→recovery` boundary MAE** (and whether MediaPipe occlusion explains it). |
| Most likely Reviewer #2 hit | Placeholder figures + unfinished leaderboard **or** single-annotator gold standard. |
| One-day improvement priority | (1) Wire or remove placeholder figures; (2) clean comparison table; (3) delete/move empty ablation; (4) one qualitative boundary figure for catch→recovery. |

---

## 6. Confidence & Go / No-Go

**Submission-ready confidence: 58 / 100.**

| Dimension | Rough score |
|-----------|------------:|
| Scientific positioning / Related Work | 80 |
| Protocol & frozen baselines (substance) | 85 |
| Results numbers (internal consistency) | 90 |
| Results presentation (figures/tables) | 40 |
| Discussion depth | 65 |
| External reproducibility / release | 45 |
| Risk of desk-reject for unfinished polish | High |

### Recommendation: **No-Go** for external journal review today

**Go** only after a short production gate:

1. No placeholder figures in the review PDF (wire or delete).  
2. Main comparison table restricted to comparable, populated rows (or clearly footnoted).  
3. Empty ablation removed from main Results.  
4. Ranking language explicitly non-inferential (already partly done—keep it).  
5. Reproducibility appendix states exactly what an external lab can and cannot obtain.

The manuscript is close. It is not yet in a form where Reviewer #2’s first impression is “careful finished benchmark paper” rather than “strong project, incomplete camera-ready.”

---

*End of final internal review.*
