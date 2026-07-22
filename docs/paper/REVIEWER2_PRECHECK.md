# Reviewer #2 pre-check (hostile read)

**Role:** Reviewer #2 — default posture is reject if the manuscript does not clear a high bar for a benchmark/methods venue.  
**Procedure:** One continuous read of the submitted narrative (Abstract → Conclusion). Thoughts logged when they arose as *Why?*, *Needs evidence*, *Unclear*, or *Revise*.  
**Not done:** rewriting the paper; verifying code execution; checking every citation page.

**Preliminary recommendation:** **Reject / major revision required before any acceptance path.**  
This is a useful engineering artifact description, but as a journal paper it currently asks the community to trust a non-public video corpus, a single annotator, empty baseline rows, and architecture comparisons without athlete-level uncertainty.

---

## Live objections (as they occurred)

### Why?

| # | Trigger in manuscript | Why? |
|---|----------------------|------|
| W1 | Abstract: “public benchmarks … remain scarce” | Why is FineGym / MultiSports / Thiele-style validation not enough of a counterexample that the scarcity claim needs careful scoping? |
| W2 | Contribution bullet: “Public release status” = pending legal review | Why is a non-releasable video corpus presented as a *dataset contribution* rather than a private study with promised release? |
| W3 | Uniqueness claim (i)–(iv) in Related Work | Why should I believe no prior combination exists without a systematic search protocol (databases, dates, query strings)? |
| W4 | B0 “cannot be implemented … unsupported assumptions” | Why freeze an empty tier in the comparison table instead of omitting it until implemented? |
| W5 | Fixed MediaPipe; no pose re-run | Why should temporal ranking be believed if pose error on this footage is never quantified? |
| W6 | Visual approximation of Cao M3–M5 bar extrema “by expert judgment” | Why call this aligned with Cao if bar extrema were not computed? |
| W7 | Primary endpoint = boundary MAE in frames; ms withheld | Why is FPS unknown in a timing benchmark? Timing without a clock is incomplete. |
| W8 | ASFormer vs MS-TCN deltas treated as noteworthy | Why discuss architecture effects when no athlete-level test is reported and seeds ≠ independent athletes? |
| W9 | “All 33 test videos exhibited non-identical segment signatures across ASFormer seeds” | Why is seed disagreement on every video presented as a finding rather than instability? |
| W10 | Coaching implications section | Why claim coaching relevance when club footage, latency, and coach UI are all declared out of scope? |
| W11 | Frame MoF = Macro F1 (0.905/0.905; 0.902/0.902) in comparison table | Why two columns with identical numbers? |

### This needs evidence

| # | Claim / implication | Evidence needed |
|---|---------------------|-----------------|
| E1 | Expert annotation is “reference standard” / labels trustworthy | Inter-annotator agreement (or at least dual annotation on a subset) |
| E2 | “No athlete or video overlap” / no leakage | Publish the automated validation method and failure cases; not only “repository validates” |
| E3 | Rebuild “verified” / checksums | Self-contained table of hashes in the paper (or appendix), not only repo prose |
| E4 | Exact LSTM thesis reproduction | Thesis report citation + metric definition identity (same class set, same windows) |
| E5 | Uniqueness / gap vs prior weightlifting CV | Structured literature search or stronger negative evidence |
| E6 | MediaPipe adequacy for snatch phases | Pose vs MOCAP / dual-system error on this or matched footage (Thiele is cited, not measured here) |
| E7 | B2/B3 ranking (ASFormer better on segment/boundary) | Athlete-level paired test or bootstrap; LOAO or multi-split |
| E8 | catch→recovery is the hard boundary | Qualitative frames / zoomed timelines + annotator uncertainty at that boundary |
| E9 | “Pending” public data still supports a benchmark paper | Clear redistribution plan, license, and what is actually downloadable today |
| E10 | Empty rows (MS-TCN++, DiffAct, CTR-GCN→TAS) | Either results or removal — placeholders are not evidence of a leaderboard |

### This is unclear

| # | Passage | Unclear what? |
|---|---------|----------------|
| U1 | “research artifact” / “comparison substrate” | What is the citable, archival unit of release (DOI, license, version)? |
| U2 | Window LSTM vs dense B2/B3 side-by-side | What should a reader conclude from incomparable columns? |
| U3 | Frame MoF vs Macro F1 | Are these the same metric mislabeled? |
| U4 | Eight-class logits vs seven supervised phases | How is `unlabeled` handled at train vs test for dense models? |
| U5 | “Canonical” / “frozen” everywhere | Frozen relative to what process? Who may change what? |
| U6 | Protocol “frame-level (infrastructure ready)” vs Results frame metrics | How were frame scores computed for dense models? |
| U7 | 856 segment files vs 208 videos | Why ~4 segment files per video? Versions? Splits of attempts? |
| U8 | Native FPS / resolution `\pending` | How were frame indices mapped to time at all? |
| U9 | Single fixed split 49/10/11 | How were athletes assigned? Stratification? Weight class? |
| U10 | Threats vs Limitations vs Future work | Why three overlapping closing sections? |

### I would ask the authors to revise this

| # | Revision ask |
|---|--------------|
| R1 | Remove empty future-model rows from leaderboard-style tables; discuss future work in text only |
| R2 | Fix or remove Frame MoF column; define every reported metric once |
| R3 | Do not present LSTM window Acc/F1 as comparable benchmark scores without a shared aggregation path—or provide that path |
| R4 | Add IAA study **or** downscope claims from “benchmark reference” to “single-annotator provisional labels” |
| R5 | Clarify public release: what is available now vs blocked; do not list pending legality as a contribution |
| R6 | Report athlete-level uncertainty for B2 vs B3 **or** explicitly demote architecture comparison to exploratory |
| R7 | Provide FPS (or justify frame-only timing as the permanent endpoint) and demographics/camera metadata |
| R8 | Cut duplicated Cao/Chen, B0, and novelty-disclaimer passages; one canonical location each |
| R9 | Make Related Work end into Dataset; stop pointing past Methods to Results |
| R10 | Replace Abstract/Conclusion clones with a Conclusion that states the empirical pattern (frame vs segment/boundary; catch→recovery) |
| R11 | Production: cite every table/figure; remove orphan floats; regenerate print-quality figures (see internal figure/table audits) |
| R12 | Move repo-path walls out of Methods/Protocol main text into appendix |

---

## Major concerns

1. **Non-public primary data with pending rights.** A benchmark paper whose defining videos cannot be redistributed, with FPS/camera/demographics unverified, fails the usual reproducibility bar the authors themselves advertise. Code + keypoints help; they do not fully substitute for auditable video when labels are visual.

2. **Single annotator, no agreement study.** Boundary MAE is the declared primary scientific endpoint. Without reliability of boundaries, ranking models on boundary error is premature.

3. **Architecture comparison without proper uncertainty.** Three seeds on one fixed split do not support claims that ASFormer improves segment/boundary metrics over MS-TCN. The manuscript admits this and still structures Results/Discussion as a model bake-off.

4. **Incomplete / misleading comparison table.** Empty B0/MS-TCN++/DiffAct/CTR-GCN rows and duplicated MoF/Macro F1 values look like an unfinished leaderboard, not a result.

5. **Label ontology construct validity.** Seven-class visual labels are explicitly not equivalent to Cao extrema or Thiele knee-angle phases, yet the paper markets biomechanical phase segmentation. Scope must be narrower or validation stronger.

6. **Contribution inflation.** “Public release status: pending” and multiple unevaluated “registered” models read as roadmap, not completed research.

---

## Minor concerns

1. Heavy repetition of frozen/canonical/reproducibility branding and Cao/Chen origin story.  
2. LSTM thesis reproduction is a software gate, not a scientific finding worthy of repeated Discussion space.  
3. Coaching implications overclaim relative to offline, competition-broadcast setting.  
4. Qualitative analysis is thin relative to the weight placed on error modes.  
5. Notation appendix defines boundary MAE in ms while Results use frames.  
6. Over-reliance on external `\repo{...}` documents for decisions that should stand in the PDF.  
7. Paper organization / “This section…” glue and Abstract≈Conclusion structure.

---

## Mandatory revisions

1. **Data access statement:** exact artifacts downloadable today; license; what remains blocked; timeline or withdrawal of “benchmark release” language.  
2. **Annotation reliability:** IAA on a subset **or** explicit downgrade of claims + sensitivity analysis.  
3. **Clean leaderboard:** only evaluated models; correct metric definitions; no duplicate MoF/F1; no empty future rows.  
4. **Comparability policy:** either implement shared frame aggregation for LSTM or remove it from the multi-metric comparison table.  
5. **Uncertainty for B2 vs B3:** athlete-level stats or multi-split **or** rewrite so the paper is protocol+dataset only, with model numbers as illustrative runs.  
6. **Timing metadata:** verify FPS or permanently justify frame units and remove “withheld ms” as if temporary.  
7. **Resolve Frame MoF mystery** (definition + numbers).  
8. **Deduplicate** Threats/Limitations/Future and Related Work positioning vs Intro contributions.

---

## Optional improvements

1. Zoomed catch→recovery qualitative figure (B2 vs B3).  
2. LOAO or secondary split.  
3. Minimal pose-quality audit on a subset.  
4. Implement or drop B0 entirely from main tables.  
5. Humanize prose (break B2/B3 symmetry; one novelty disclaimer).  
6. Shorten Protocol YAML narrative; move paths to appendix.  
7. Merge per-class recall tables.

---

## Overall confidence

**Confidence in this review: 4 / 5**  
(High confidence on structural/scientific reporting gaps visible from the PDF narrative; not a full re-implementation audit.)

**Confidence that the current manuscript is ready for acceptance: 1 / 5**

---

## Probability of acceptance after revision

| Scenario | Approx. probability |
|----------|---------------------|
| Cosmetic edits only | **~5–10%** |
| Mandatory revisions 1–8 completed, data still not public but labels+keypoints+code clearly licensed and IAA added | **~35–45%** (venue-dependent; still an uphill “benchmark” claim) |
| Mandatory revisions + public video (or strong legal subset) + athlete-level uncertainty + cleaned tables | **~55–70%** |

**Point estimate after serious revision:** **~40%** acceptance at a selective journal/conference that expects public benchmarks; **lower** if marketed as biomechanics validation; **higher** if repositioned as a reproducibility/systems paper with modest empirical claims.

---

## Bottom line (Reviewer #2)

The manuscript documents careful engineering and honest limitations, but honesty about missing IAA, missing FPS, missing public video, and missing significance tests does **not** neutralize those gaps—it highlights them. I would vote **reject** in the present form, with an invitation to resubmit only after the mandatory revisions above make the “benchmark” claim operationally true.

---

*End of Reviewer #2 pre-check.*
