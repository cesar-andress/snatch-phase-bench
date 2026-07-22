# Related Work — Final Editorial Check

**Date:** 2026-07-22  
**Scope:** Editorial / bibliographic consistency of Related Work before journal submission.  
**Constraint:** No new literature search except citation verification. No changes to experiments, figures, result tables, or numeric claims.

**Manuscript compile:** `paper/main.pdf` — OK (latexmk, 30 pages).

---

## Final recommendation

**READY FOR SUBMISSION**

(Related Work and bibliography are scientifically consistent for Q1 review on the points audited below.)

---

## 1. Bibliography issues found

| Key | Issue | Action |
|-----|--------|--------|
| `li2020mspp` (MS-TCN++) | Wrong DOI (`…3030337` → 404); first author spelled `Shujie`; co-author `Yang Liu`; missing volume/pages | Corrected DOI `10.1109/TPAMI.2020.3021756`; authors `Shijie Li`, `Yun Liu`; vol.~45(6):6647--6658 |
| `uhlrich2023opencap` | Wrong DOI (`…1011460` resolved to a different PLOS Comp Biol article); author list matched an earlier/alternate authorship set | Corrected DOI `10.1371/journal.pcbi.1011462`; authors updated to published record; pages `e1011462` |
| `shah2026barbell` | Missing DOI; `note` asked to “verify final publication metadata” | DOI added `10.1007/s42979-026-04875-z`; verify-note removed (Crossref + OpenAlex agree: *SN Computer Science* 7(4), 2026) |

No duplicated BibTeX keys. No missing keys among Related Work / prior-art table cites. PDF bibliography compiles cleanly.

---

## 2. Citations corrected

- `li2020mspp` — metadata and DOI aligned with IEEE TPAMI record.
- `uhlrich2023opencap` — DOI and authorship aligned with PLOS Computational Biology published article.
- `shah2026barbell` — DOI added; retained (verified publication).

---

## 3. Citations removed

**None.**

`shah2026barbell` was retained after verification (not removed).

---

## 4. `shah2026barbell` status

| Field | Verified value |
|-------|----------------|
| Title | Single-Camera Barbell Trajectory Analysis for the Snatch Lift |
| Authors | Shah, Raval, Taber, Kaya, Maddox, Raval |
| Year | 2026 |
| Venue | SN Computer Science |
| Volume / issue | 7 / 4 |
| Article / pages | 297 |
| DOI | 10.1007/s42979-026-04875-z |

**Decision:** **KEEP** — bibliographically stable enough for citation (Crossref + OpenAlex). Used only as a barbell-trajectory neighbour (no phase-label claim attributed to it).

---

## 5. Tool-specific language removed

| Location | Before | After |
|----------|--------|-------|
| Research gap (`02_related_work.tex`) | “To the best of our **OpenAlex-backed** literature review…” | “To the best of our literature review…” |

Manuscript-wide grep: **no** remaining `OpenAlex`, “API-assisted”, or similar tool wording.

---

## 6. Novelty / gap wording softened

| Change | Rationale |
|--------|-----------|
| Sports subsection: “They do not release…” → “Closest public datasets address related… but they do not provide…” | Avoid absolute “do not exist / never released” tone |
| Gap lead-in rewritten to name typical foci (action recognition, sports understanding, procedural TAS, pose, biomechanics) | Reviewer-robust framing of *combination* gap |
| Gap close: “targets that remaining intersection” → “combines Olympic snatch… frame-level… markerless pose… standardized TAS… reproducible baseline protocol” | Motivates artifact without promotional uniqueness claims |
| Abstract: “remain scarce” → “remain limited” (+ explicit “markerless pose”) | Softens absolute scarcity claim; aligns terminology |

No “first ever / unique / unprecedented / only dataset / no benchmark exists” claims remain in Related Work.

---

## 7. Consistency fixes (cross-section)

| Term | Abstract / Intro / RW / Discussion / Conclusion |
|------|--------------------------------------------------|
| temporal action segmentation / `\ac{TAS}` | Keywords + RW + Discussion (`\ac{TAS}` metrics) |
| temporal / snatch phase segmentation | Abstract, Intro subsection, RW gap |
| markerless pose | Abstract softened wording; RW pose + gap |
| Olympic weightlifting / snatch | Title, Abstract, RW opening and gap |
| benchmark / protocol / frame-level / boundary | Consistent; contribution framed as protocol, not architecture |
| Discussion | “TAS-style metrics” → “`\ac{TAS}` metrics” |

---

## 8. Length control

| Metric | Before polish | After |
|--------|---------------|-------|
| Word count (`02_related_work.tex`) | ~1029 | ~1055 (**+2.5%**) |

Within the ≈10% budget.

---

## 9. Reviewer #2 stress test (addressed)

| Challenge | Response in text |
|-----------|------------------|
| “Is this the first snatch TAS benchmark?” | Claim is combination-scoped: “to the best of our literature review, we did not identify… that **jointly** provides…” |
| “What about FineGym / FineDiving / MultiSports / Breakfast?” | Explicitly named as closest neighbours with differing axes |
| “What about Shah / Chen barbell CV?” | Cited as trajectory/scoring neighbours without phase-TAS protocol |
| “OpenAlex / search tooling?” | Removed from manuscript |

---

## 10. Files touched

**Manuscript (outside software Git root may differ):**

- `paper/sections/02_related_work.tex`
- `paper/bibliography.bib`
- `paper/main.tex` (Abstract novelty soften)
- `paper/sections/07_discussion.tex` (TAS terminology)

**This report:**

- `docs/paper/RELATED_WORK_FINAL_CHECK.md`

**Not modified:** experiments, figures, result tables, numeric results, frozen B1/B2/B3 artifacts.

---

## 11. Residual non-blocking notes (not blocking “READY”)

- Several older conference entries still lack DOIs in the `.bib` (OpenPose, NTU, Breakfast, etc.); venues/years are standard and accepted; adding DOIs is optional polish, not a Related Work integrity failure.
- `pages = {297}` for Shah is Springer-style article numbering; Crossref did not expose a page range — consistent with SN Computer Science article IDs.
