# Global repetition audit — SnatchPhaseBench manuscript

**Date:** 2026-07-22  
**Scope:** Abstract (`main.tex`) + `sections/*.tex` + in-build appendices. Captions/tables checked only when they repeat body claims.  
**Method:** Phrase inventory + near-duplicate sentence matching + manual review.  
**False-positive filter:** Domain terms required by the topic (`benchmark`, `MediaPipe`, phase names, B2/B3) are **not** findings unless stacked into formulaic prose. Parallel metric reporting for two models is noted only when it reads as copy-paste rather than necessary parallelism.

---

## Executive verdict

Classic LLM transition glue is **largely absent** (`Furthermore` / `Moreover` / `Additionally` / `Overall` / `This demonstrates|suggests|highlights|indicates` ≈ **0** hits).  
Quality is reduced instead by **claim recycling across Abstract → Intro → Related Work → Discussion → Conclusion → Limitations**, plus a heavy **frozen / canonical / verified / reproducible** drumbeat.

---

## Findings by severity

### Severity 1 — High (noticeably reduces quality; cut or localize)

#### S1.1 “Not an architecture paper / no novelty” claim (3–4×)

| Location | Form |
|----------|------|
| Abstract | “contribution is a reproducible benchmark protocol rather than a new architecture” |
| Related Work positioning | “It is not an architecture paper” + “methodological novelty, which is not claimed” |
| Conclusion | “not as a claim of architectural novelty” |
| Intro (near) | “reproducibility-oriented benchmark rather than a one-off model description” |

**Why problematic.** The same epistemic disclaimer is restated as a conclusion in multiple sections, which reads as template caution rather than progressive argument.

**Recommendation.** Keep **one** strong instance (prefer Abstract *or* Conclusion). Elsewhere replace with a forward pointer (“as framed in the Abstract”) or delete.

---

#### S1.2 B0 “exploratory / unsupported assumptions” explanation (4–5×)

Repeated in Related Work positioning, Methods §B0, Results benchmark blurb, Discussion threats, Limitations incomplete-leaderboard item (and table caption).

**Why problematic.** Full causal explanation (“cannot be implemented from knee angles alone without unsupported assumptions”) is re-taught instead of cited once.

**Recommendation.** Full explanation only in **Methods §B0**. Elsewhere: “B0 remains exploratory (\Cref{sec:methods:b0})” — one clause.

---

#### S1.3 Cao / Chen taxonomy + visual-boundary story (4+ sections)

Full or partial retellings in Related Work (primary sources + positioning), Dataset taxonomy, Methods annotation (long transition list), Protocol ontology paragraph, Discussion construct validity.

**Why problematic.** Readers meet the same origin story repeatedly; Methods already enumerates every transition.

**Recommendation.** Canonical detail in **Dataset taxonomy + Methods annotation**. Related Work keeps literature contrast only; Protocol/Discussion cite `\Cref{sec:dataset:taxonomy,sec:methods:annotation}` without re-listing M1–M6 / six named phases.

---

#### S1.4 Abstract / Intro / Conclusion contribution stack

Near-parallel package:

- curated dataset + athlete-disjoint splits + frozen preprocessing + shared evaluation  
- LSTM reproduction / rebuild checksums  
- MS-TCN + ASFormer under shared multi-seed protocol with frame / segment / boundary metrics  

**Why problematic.** Conclusion largely restates Abstract + Intro Scope; little new synthesis.

**Recommendation.** Conclusion: **2–3 sentences** of takeaway (what the dense results imply for boundary-centric evaluation) + one release caveat. Drop the second full inventory of components.

---

### Severity 2 — Medium (audible formula; thin selectively)

#### S2.1 Lexical drumbeat: `frozen` (~45), `verified` (~31), `canonical` (~22), `reproducib*` (~20)

Often stacked in one sentence (“frozen … canonical … verified … shared protocol”).

**Why problematic.** Reproducibility is a real contribution, but the adjectives become filler and sound LLM-guardrail-heavy.

**Recommendation.** Prefer **nouns of evidence** once per section (checksum match, locked config, identical seeds) over repeating the adjectives. Cap at ~1–2 of {frozen, canonical, verified} per paragraph.

---

#### S2.2 Inter-annotator / single-annotator caveat (3×)

Dataset annotations, Methods annotation closing sentence, Limitations item (Discussion threats also mentions single-annotation).

**Recommendation.** State once in Dataset; Limitations keeps a short bullet with `\Cref`; delete the Methods echo.

---

#### S2.3 Window-overlap / accuracy-overstates-generalization (2–3×)

Protocol overlap subsection, Discussion overlap, Limitations “Window-level historical baseline”.

**Recommendation.** Keep Protocol definition + one interpretive sentence in Discussion; Limitations bullet can be a cross-ref only.

---

#### S2.4 “This section …” openings (4×)

Dataset, Protocol, Results, Related Work closing.

**Why problematic.** Mild LLM/section-template smell; low information.

**Recommendation.** Delete or replace with a concrete topic sentence (what the section *decides*, not that it “reports”).

---

#### S2.5 Discussion restates Results numbers

Discussion §Interpretation reprints mean F1@50 / MAE already given in Results (and again summarized in §Benchmark comparison).

**Recommendation.** Discussion: interpret deltas and failure modes; cite tables instead of re-listing the same means unless needed for a contrast claim.

---

#### S2.6 “Under [a|the|an identical] shared / multi-seed protocol …” (many)

Abstract, Intro, Results, Discussion, Conclusion, captions.

**Recommendation.** Define once in Protocol; later say “under the B2/B3 protocol (\Cref{sec:protocol:benchmark})”.

---

### Severity 3 — Low (optional polish)

#### S3.1 Parallel Results templates (acceptable but stiff)

Identical “Across seeds, test frame macro-F1 was … segment F1@50 was … edit score … boundary MAE … boundary F1 …” for MS-TCN then ASFormer; mirrored “mean per-class recall was lowest for…” sentences.

**Note.** Parallelism aids comparison; still reads machine-generated if both blocks stay verbatim.

**Recommendation.** Keep numbers in tables; prose for the second model can be shorter (“ASFormer means appear in \Cref{tab:asformer_seed_stability}; relative deltas vs B2 are …”).

---

#### S3.2 `therefore` (5×)

Legitimate causal connectives; **not** an LLM pile-up. No action required unless a local sentence already follows from the previous clause.

---

#### S3.3 Methods boilerplate lines

Repeated “Implementation: `src/...`; configuration: `configs/...`” pattern for B2/B3.

**Recommendation.** One sentence + appendix/repo pointer.

---

## Explicit non-findings (avoided false positives)

| Pattern | Why not reported |
|---------|------------------|
| `Furthermore` / `Moreover` / `Additionally` / `Overall` / `In summary` | Effectively unused |
| `This demonstrates/suggests/highlights/indicates` | Unused |
| High count of `benchmark`, phase names, model names | Required technical vocabulary |
| Listing both B2 and B3 metrics | Necessary scientific content |
| `catch→recovery` in Results + Discussion | Primary finding; one recall in Discussion is appropriate |

---

## Priority edit order

1. Collapse novelty / “not architecture” disclaimers to a single locus.  
2. Collapse B0 and Cao/Chen explanations to Methods/Dataset with cross-refs.  
3. Rewrite Conclusion so it does not clone Abstract.  
4. Thin `frozen`/`canonical`/`verified` stacking; trim “This section” openers.  
5. Optional: shorten second Results seed paragraph and Methods path boilerplate.

**Do not change experimental numbers** while applying these edits.

---

*End of repetition audit.*
