# Coherence review — section-to-section flow

**Date:** 2026-07-22  
**Mode:** Read-only (no manuscript edits).  
**Actual section order in `main.tex`:**  
Abstract → Introduction → Related Work → **Dataset** → Methods → Experimental Protocol → Results → Discussion (**incl. Threats to Validity** + Future work) → **Limitations** → Conclusion.

The checklist below follows the requested spine and inserts **Dataset** and **Limitations** where the PDF actually places them. “Threats to Validity” is a **Discussion subsection**, not a top-level section.

---

## Chain verdict (summary)

| Transition | Natural lead-in? | Main issue |
|------------|:----------------:|------------|
| Abstract → Introduction | Partial | Abstract already states verification + B2/B3; Intro restarts full motivation |
| Introduction → Related Work | Yes | Models named before literature justifies them (mild) |
| Related Work → Dataset | **Weak** | Related closes toward Results; skips Dataset bridge |
| Dataset → Methods | Partial | Annotation story split; Methods cites Protocol early |
| Methods → Experimental Protocol | Partial | Heavy overlap; Protocol opens as repo docs, not as next logical question |
| Experimental Protocol → Results | Yes | Results opener wrongly implies Dataset is inside Results |
| Results → Discussion | Partial | Discussion re-reports Results before interpreting |
| Discussion → Threats | Yes | Threats fit; then Future work before Limitations feels early |
| Threats / Future → Limitations | **Weak** | Near-duplicate caveats; two closing “limits” blocks |
| Limitations → Conclusion | Weak | Conclusion ignores Discussion findings; clones Abstract |

Overall: the scientific arc is recoverable, but several junctions **re-motivate**, **skip the next section**, or **close before the argument has used the Results**.

---

## Transition-by-transition

### Abstract → Introduction

**What works.** Abstract states problem (phase ID, scarce reproducible benchmarks) and names the artifact; Introduction correctly expands snatch, coaching need, MOCAP vs markerless, TAS, reproducibility gap.

**Abrupt / missing links.** None severe.

**Repeated motivation.** Expert labeling cost + markerless alternative + reproducibility gap appear in both.

**Claims too early (for a linear reading).** Abstract already asserts verified rebuild counts, leakage-free splits, exact LSTM reproduction, and completed multi-seed MS-TCN/ASFormer evaluation—before any method or protocol. Acceptable for an abstract, but it forces Introduction to either repeat or feel like a second abstract.

**Concepts too late.** None here.

---

### Introduction → Related Work

**What works.** Intro ends with Paper organization pointing to Related Work; TAS and reproducibility gap set up the literature map.

**Claims too early.** Intro Scope/Contributions already freeze B1/B2/B3, window counts, and “identical seeds… early-stopping” before Related Work argues why MS-TCN/ASFormer are the right comparison class, and before Dataset defines the ontology those models train on.

**Missing links.** Intro motivation for coaching is not explicitly handed off as “Related Work will show no public snatch phase benchmark on pose”; Related Work opens by defining SnatchPhaseBench again instead of continuing the gap sentence.

---

### Related Work → Dataset  
*(requested chain jumped here to Methods; Dataset is the real next section)*

**Abrupt transition.** Related Work positioning closes with “This section motivates… `\Cref{sec:results}` reports…”, **skipping Dataset and Methods**. The reader is pointed past the next two sections.

**Repeated motivation.** Positioning re-lists contributions, “not an architecture paper,” B0 exploratory story, and Cao/Chen taxonomy—material already in Intro Contributions and Primary sources.

**Missing link.** No sentence of the form: “The following section describes the labeled corpus that makes that protocol concrete.”

**Claims too early.** Gap claim “(i)–(iv) no single prior artifact…” and B0 “unsupported assumptions” are asserted before Dataset/Methods evidence is shown (Methods later carries the B0 audit detail).

**Concepts too late.** Boundary-centric evaluation is promised; the dataset’s segment files and transition inventory that make boundary metrics possible are only fully concrete in Dataset/Protocol.

---

### Dataset → Methods

**What works.** Dataset supplies counts, taxonomy, splits, pose; Methods opens with supervised labeling from fixed pose—logical.

**Abrupt / duplicated.** Methods §Annotation re-tells single-annotator + Cao/Chen boundary list after Dataset §Annotations already described the labeling process (without the full transition catalog). Feels like a rewind, not a lead-in.

**Missing link.** Dataset ends on window construction / notation; Methods does not open by saying “given those windows and dense sequences, models do X.” Problem formulation jumps to math without a one-line handoff.

**Concepts too late.** Detailed visual boundary criteria appear in Methods after taxonomy tables; a reader of Dataset alone cannot yet operationalize transitions. Conversely, Methods cites `\Cref{sec:protocol:metrics}` and `\Cref{sec:protocol:benchmark}` **before** Protocol—forward dependency that breaks linear “naturally leads to next.”

**Claims too early.** Methods already states B2/B3 freezing and “shared evaluator” while Protocol is where locks are supposed to be specified.

---

### Methods → Experimental Protocol

**What works.** Methods defines models; Protocol should define how they are trained/evaluated—correct order in principle.

**Abrupt transition.** Protocol opens with YAML paths, snapshot dirs, and Zenodo pending—operations manual—rather than the natural next question after Methods (“How are B1 vs B2/B3 scored fairly?”).

**Repeated motivation / explanations.** Cao/Chen ontology and MS-TCN design deviations reappear in Protocol §Configuration after Methods §Benchmark models.

**Missing links.** Clear bridge sentence missing: “The following protocol freezes seeds, hardware, early stopping, and metrics so B2 and B3 are comparable.”  
Frame-level granularity is labeled “infrastructure ready” in Protocol while Results later report frame macro-F1 for dense models—reader may not see how “ready” became “reported” without a tighter Methods↔Protocol↔Results link.

**Concepts too late.** Primary endpoints (segment F1@50 for selection; boundary MAE) are pinned in Protocol §Stats near the **end**, after long config/hardware material; they should conceptually precede Results but feel buried.

**Claims too early.** “Future models must not alter frozen B2/B3 numbers” is a process claim before Results show those numbers.

---

### Experimental Protocol → Results

**What works.** Protocol defines multi-seed locks; Results delivers seed tables—good causal order.

**Abrupt / inaccurate opener.** Results first sentence claims it reports “verified dataset statistics (`\Cref{sec:dataset}`)”—dataset stats already appeared; Results does not newly establish them. Soft discontinuity.

**Missing link.** Protocol §Ablations says none are reported; Results never acknowledges that gap (fine scientifically, but the planned-ablation subsection dead-ends into silence).

**Claims too early.** Benchmark comparison table appears before the narrative seed sections that justify the means—readable, but the comparison is introduced before the reader has seen per-seed stability prose.

---

### Results → Discussion

**What works.** Results supply B2/B3 metrics and catch→recovery; Discussion can interpret.

**Abrupt / repetitive.** Discussion §Interpretation **restarts** with exact LSTM reproduction and class imbalance—Dataset/Results already established this—before reaching dense-model interpretation.

**Missing links.** Little handoff from qualitative error section to Discussion practice implications (catch→recovery appears again but without building on the qualitative figure/timeline).

**Unsupported stretch (mild).** “Confusion between adjacent phases … is expected” is plausible but not tightly tied to a shown confusion analysis in Results prose (figure may exist; text does not walk the reader there).

---

### Discussion → Threats to Validity → (Future work)

**What works.** Threats subsection is the right place for internal/external/construct validity after interpretation.

**Abrupt.** Future work follows Threats **inside Discussion**, then a full **Limitations** section repeats many of the same points—reader experiences two consecutive “what’s wrong / what’s missing” landings.

**Repeated motivation.** B0 exploratory, taxonomy vs knee-angle, single cohort, IAA, overlap—reappear from Dataset/Methods/Protocol.

**Missing link to Conclusion.** Future work lists priorities; Conclusion restates open release/IAA without connecting to the scientific finding (boundary errors, B2 vs B3).

---

### Threats / Future work → Limitations → Conclusion  
*(requested “Threats → Conclusion” skips Limitations, which exists)*

**Abrupt.** Limitations is largely a bullet remix of Threats + Dataset caveats + Protocol stats gap—feels like a second ending before Conclusion.

**Conclusion unsupported by previous sections (argumentatively).**  
Supported: rebuild/LSTM gate; B2/B3 under shared protocol; not an architecture paper; public video still open.  
**Not carried forward:** Discussion’s actual interpretive payload (frame macro-F1 ≈ flat while segment/boundary differ; catch→recovery dominates MAE; descriptive-only seed summaries). Conclusion reads as Abstract reprise, not as closure of the Results→Discussion arc.

**Claims too early / recycled.** “Not architectural novelty” closes a paper whose Discussion never argued for an architecture claim in the first place—disclaimer without preceding temptation.

---

## Cross-cutting coherence issues

### Repeated motivation (global)

1. Scarce reproducible weightlifting phase benchmarks (Abstract, Intro, Related, Discussion prior-work).  
2. Reproducibility / checksum / frozen protocol branding (almost every section).  
3. Cao/Chen + setup taxonomy (Related, Dataset, Methods, Protocol, Discussion construct validity).  
4. B0 exploratory / unimplemented (Related, Methods, Results, Discussion, Limitations).  
5. Single annotator / no IAA (Dataset, Methods, Discussion threats, Limitations, Conclusion).

### Missing links (global)

- Related → Dataset handoff.  
- Methods → Protocol handoff (why locks matter).  
- Results findings → Conclusion (no takeaway sentence).  
- Threats vs Limitations division of labor unexplained.

### Claims introduced too early

| Claim | First appears | Better after |
|-------|---------------|--------------|
| Exact LSTM reproduction + rebuild | Abstract | Results §Baseline (Abstract may preview lightly) |
| Frozen B2/B3 under identical locks | Intro Contributions | Protocol + Results |
| Uniqueness (i)–(iv) | Related Work | After Dataset+Protocol facts |
| B0 impossible without unsupported assumptions | Related Work | Methods §B0 |
| Primary endpoint = boundary MAE / F1@50 | Scattered early; formalized late in Protocol | Immediately after metric definitions, before Results |

### Concepts introduced too late

| Concept | Appears late relative to use |
|---------|------------------------------|
| Operational boundary placement rules | Methods (after taxonomy elsewhere) |
| Formal primary endpoints & “no athlete-level tests” | End of Protocol |
| How frame metrics are obtained for dense models vs “infrastructure ready” window aggregation | Never tightly sequenced |
| Dataset as first results object | Results claims it; content lived in Dataset |

### Conclusions unsupported by previous sections

| Closing statement | Support status |
|-------------------|----------------|
| Artifact is comparison substrate, not novelty | Supported by framing; unsupported as a *result* of Discussion |
| B2/B3 “supply” dense metrics | Supported by Results |
| Public video + multi-annotator remain open | Supported by Limitations/Dataset |
| Implicit “mission accomplished” tone without naming the main empirical pattern | **Weak** — Discussion findings not concluded |

---

## What already coheres well

- Intro learning-problem → Related TAS/sports CV contrast.  
- Dataset splits/imbalance → Protocol overlap warning → Discussion overlap (when not duplicated excessively).  
- Protocol multi-seed locks → Results seed tables.  
- Results catch→recovery MAE → Discussion practice + boundary emphasis.  
- Threats construct validity ↔ Dataset taxonomy honesty.

---

## Priority fixes (guidance only; not applied here)

1. End Related Work by pointing to **Dataset**, not Results.  
2. Open Protocol with the fairness question; move YAML detail down.  
3. Decide Threats vs Limitations: keep one narrative home for caveats.  
4. Rewrite Conclusion from Discussion takeaways (segment/boundary vs frame; catch→recovery), not Abstract inventory.  
5. Trim repeated Cao/Chen, B0, and IAA to a single canonical section each with cross-refs.

---

*End of coherence review.*
