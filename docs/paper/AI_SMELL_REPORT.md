# AI-assistance writing smell report

**Date:** 2026-07-22  
**Lens:** Patterns that a skeptical reviewer might read as LLM-assisted prose.  
**Out of scope:** Scientific correctness, completeness of experiments, citation coverage.  
**Companion:** [`REPETITION_AUDIT.md`](REPETITION_AUDIT.md) (overlap is intentional; this report focuses on *voice*, not inventory of repeated facts).

---

## Overall impression

The manuscript mostly avoids flashy LLM tells (`Furthermore`, `Moreover`, `This highlights`, “state-of-the-art”, “comprehensive framework”).  
What still sounds artificial is **editorial over-regularity**: matched sentence lengths, mirrored section templates, stacked hedge-disclaimers, product-brochure nouns (`artifact`, `stack`, `substrate`), and conclusions that restate the Abstract instead of ending an argument.

Experienced researchers usually vary rhythm, leave some asymmetry between model write-ups, and put caveats once.

---

## Issues (by how strongly they read as AI-assisted)

### 1. Formulaic conclusion that clones the Abstract  
**Where:** Abstract closing + `09_conclusion.tex` (and near-echo in Intro “Scope”).

**Why it sounds artificial.** Classic LLM wrap-up: inventory of components → protocol sentence → “not a claim of architectural novelty” → open issues. Same cadence and disclaimer packaging as the Abstract, as if a template “Conclusion” was regenerated.

**Make it human.** End with one concrete takeaway a reader did not already get (e.g. boundary MAE still dominated by catch→recovery; frame scores alone are misleading). Drop the novelty disclaimer if Abstract already has it. Do not re-list dataset + splits + preprocessing.

---

### 2. Excessive symmetry between B2 and B3 Results blocks  
**Where:** `06_results.tex` MS-TCN vs ASFormer subsections; mirrored “Across seeds, test frame macro-F1 was … segment F1@50 was … edit score … boundary MAE … boundary F1 …”; twin “mean per-class recall was lowest for…” sentences.

**Why it sounds artificial.** Near-isomorphic paragraphs with only numbers swapped is a hallmark of generated “report both models fairly” prose. Human write-ups usually narrate the first model fully and compress the second into deltas + table cites.

**Make it human.** Keep full metric list once (or only in tables). For B3: “Means in \Cref{tab:asformer_seed_stability}; vs B2, segment F1@50 rises by … while frame macro-F1 is essentially unchanged.” Vary which error mode you emphasize per model.

---

### 3. Overly regular sentence rhythm in Intro / Discussion openers  
**Where:** Intro opening triad (~20–26 words each); Discussion interpretation paragraph (four consecutive ~21–24-word sentences, near-zero length variance).

**Why it sounds artificial.** LLM drafts often emit “smooth” medium-length declaratives with similar clause structure (subject → verb → complement → cite). Spoken academic English mixes short punches with longer asides.

**Make it human.** Break one sentence; start another with a fragment or a concrete noun (“Transition windows are scarce.”). Move a cite mid-clause. Allow an abrupt one-liner after a dense sentence.

---

### 4. Repetitive paragraph / subsection structure  
**Where:** Related Work topic sections often follow: define area → cite 2–3 systems → “these studies clarify X” → “they do not provide Y / SnatchPhaseBench is not Z”. Discussion uses a checklist of tiny subsections each ending in a scope or caveat line. Intro “Paper organization” is a perfect `\Cref{sec:…} Verb …` march.

**Why it sounds artificial.** The dialectic template (survey → gap → our artifact) repeats until the section feels generated. Paper-organization marches are especially associated with LLM boilerplate.

**Make it human.** Merge two Related Work closing contrasts into one paragraph. Delete or shrink Paper organization to two sentences. In Discussion, combine “Prior work” and “Practice” if each is only 2–3 lines, or replace subsection headers with flowing prose.

---

### 5. Predictable transitions and section glue  
**Where:** “This section reports/specifies/motivates…”; “Under a/the/an identical shared multi-seed protocol…”; “At the same time,”; stacked “therefore” in mild causal chains; Related Work “In order of defensibility, the contributions are…”

**Why it sounds artificial.** Meta-transitions announce structure instead of arguing. “In order of defensibility” is especially unnatural in a journal Related Work—it sounds like an internal review rubric leaked into the paper.

**Make it human.** Cut “This section…” openers. Define the shared protocol once and later write “on the locked B2/B3 recipe.” Replace the defensibility list with a blunt ranking in ordinary English (“The data and evaluator matter more here than a new backbone.”).

---

### 6. Unnecessary summaries and self-positioning disclaimers  
**Where:** Repeated “not an architecture paper / methodological novelty is not claimed / rather than a new architecture”; Related Work closing that re-summarizes contributions already in Intro; Discussion sentences that only restate table means.

**Why it sounds artificial.** LLMs over-insure against overclaiming. Human authors state the scope once and move on; repeating the disclaimer reads like safety fine-tuning, not scientific voice.

**Make it human.** One disclaimer total. Discussion should interpret (why catch→recovery fails; what seed variance means), not recapitulate Results.

---

### 7. Generic academic filler / brochure nouns  
**Where:** “research artifact”, “reproducibility-oriented evaluation framework”, “canonical evaluation stack”, “comparison substrate”, “present artifact contributes”, “verified state of SnatchPhaseBench”, Abstract triad “curated … documented … reproducibility-oriented”.

**Why it sounds artificial.** Product-copy cadence: stacked adjectival nouns with little concrete content. Experienced writers name the thing (“208 labeled lifts, fixed split, shared evaluator”).

**Make it human.** Prefer countable deliverables over “framework/stack/substrate/artifact.” Example: “We release labels, a fixed athlete split, and an evaluator that scores segment F1 and boundary MAE.”

---

### 8. Passive-heavy “status report” voice  
**Where:** Abstract and Scope (“are evaluated”, “has been verified”, “is retained”); Methods/Protocol status sentences; ~20%+ of sentences use be + past participle or “is treated/retained/reported” constructions.

**Why it sounds artificial.** Continuous passive status language flattens agency and resembles generated documentation. Not every passive is wrong (methods often need it), but page-long retention of “X is frozen / Y is verified / Z is retained” feels machine-edited for neutrality.

**Make it human.** Alternate with active verbs where true: “We freeze B2 weights,” “Checkpoint evaluation matches the thesis report,” “Annotators placed boundaries at …” Keep passive for procedures without a clear actor.

---

### 9. Unnatural wording / reviewese  
**Where:** “fine-grained, single-actor, short-horizon” adjective pile-up; “phase-boundary quality can be measured”; “in order of defensibility”; “Highest-priority extensions include A, B, C, D, and E”; “First-pass diagnostics flagged…”; Contribution bullet titles in Title Case marketing labels (“Canonical evaluation stack”).

**Why it sounds artificial.** Hyphenated trait lists and “diagnostics flagged” sound like internal tickets or model self-description, not lab prose. Bullet titles that brand every contribution are common in LLM contribution blocks.

**Make it human.** Use one characterizing phrase, then evidence. Future work: pick two priorities and say why. Soften contribution bullets to plain sentences without slogan headers, or keep fewer bold leads.

---

### 10. Marketing / certainty tones (mild, but present)  
**Where:** “technically demanding”; “gold standard”; “matured rapidly”; “biomechanically critical”; “coaching-relevant”; Abstract “requires reliable identification”; “exact reproduction” / “reproduces … exactly” stacked with reproducibility branding.

**Why it sounds artificial.** Mild brochure emphasis plus absolute exactness language, even when the paper elsewhere hedges carefully. Reviewers associate “exact / reliable / critical / matured rapidly” clusters with polished LLM abstracts.

**Make it human.** Prefer measured claims: “labels match the thesis report on the rebuilt test set,” “MOCAP remains the laboratory reference,” “short phases matter for coaching cues.” Save intensifiers for one place only.

---

### 11. Excessive certainty in framing vs hedge stacking elsewhere  
**Where:** Certainty: rebuild/reproduction “exactly”; gap claims that “no single prior artifact jointly provides (i)–(iv)”. Hedge stacking: “No claim is made that…”, “descriptive seed-level summaries”, “remain open”, “partial” alignment repeated across Discussion/Limitations.

**Why it sounds artificial.** The combination of sweeping uniqueness lists and repeated legalistic hedges is a known LLM pattern: bold positioning + safety epilogue.

**Make it human.** Soften the uniqueness list to “we do not know of a public athlete-disjoint snatch phase benchmark on fixed pose with shared TAS metrics.” State hedges once in Limitations; do not re-litigate them after every positive sentence.

---

## What does *not* strongly smell of AI (for balance)

- Sparse use of classic transition macros (`Furthermore`, `Moreover`, `Additionally`, `Overall`, `This demonstrates`).  
- Related Work citations to specific events (M1–M6, Theia3D offsets) read like domain knowledge, not pure filler.  
- Limitations as a concrete bullet list is normal for this venue; smell appears when the same caveats are also sermonized in Discussion.

---

## Practical rewrite priorities (voice only)

1. Rewrite Conclusion so it cannot be mistaken for a second Abstract.  
2. Break B2/B3 symmetry in Results prose.  
3. Delete Paper-organization march and “This section…” glue.  
4. Replace artifact/stack/substrate language with concrete nouns.  
5. Keep one novelty/scope disclaimer; delete the rest.  
6. Vary sentence length in Intro opening and Discussion interpretation.

No experimental numbers need change for these edits.

---

*End of AI smell report.*
