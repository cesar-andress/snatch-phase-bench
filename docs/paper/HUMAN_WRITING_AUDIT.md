# Human writing audit

**Date:** 2026-07-22  
**Scope:** Stylistic voice only (Abstract + main sections).  
**Not in scope:** Science, literature coverage, LaTeX engineering, experiments, figures/tables of numbers, citation keys.

**Compile check:** `paper/main.pdf` rebuilt successfully after edits (30 pages).

---

## Confirmation: scientific content unchanged

No numbers, results, equations, citation keys, figure files, or result-table values were modified.
Terminology and claims were preserved.
Edits were limited to wording, sentence breaks, emphasis markup, and removal of AI-typical glue phrases.

---

## First-person counts

| Form | Before (main prose) | After |
|------|---------------------|-------|
| `we` / `We` | 3 (`we did not identify`; `we apply`; `We draw`) | **0** |
| `our` | 1 (`our literature review`) | **0** |
| `us` | 0 | **0** |
| `I` | 0 (true first person) | **0** |

False positives such as math indices `$i$` were ignored.

### Remaining intentional first-person usages

**None.** Gap and bootstrap statements were rewritten in neutral scientific voice:

- “To the best of our literature review, we did not identify…” → “No publicly available benchmark was identified…”
- “we apply the paired bootstrap…” → “Athlete-level uncertainty … is quantified with the paired bootstrap…”
- “We draw 10,000 such samples…” → “Ten thousand such samples are drawn…”

---

## Stylistic changes made

### Punctuation / LLM glue
- Removed prose em-dash constructions (`---` as parenthetical interrupters), especially in Discussion (class-imbalance sentence).
- Replaced prose double hyphens with natural wording (`bar--body` → `bar-body`; `M1--M6` → `M1 to M6`; epoch/runtime ranges written as “from … to …”).
- Split semicolon-heavy and colon-catalog sentences into shorter declaratives (Related Work, Results ASFormer block, Protocol bootstrap paragraph, Limitations).
- Removed transition `In addition` before the bootstrap protocol paragraph.

### AI-smell / brochure nouns
- Abstract: “curated … artifact … evaluation stack” → concrete “labeled snatch attempts … shared evaluator”.
- Abstract/Conclusion: dropped mirrored “contribution is not a new architecture” wrap-up clone; Conclusion now ends on the concrete catch→recovery / bootstrap takeaway.
- Softened “offers a practical alternative” / “provide dense … baselines”.
- Intro: “protocol-first artifact” → “locked evaluation protocol”.
- Discussion: removed the repeated “primary contribution remains the benchmark protocol…” disclaimer (already stated in Abstract).

### Emphasis
- Removed `\textbf{…}` labels from Contributions, Evaluation strategy, Baseline evaluation modes, and Limitations item heads.
- Removed decorative `\emph{…}` on technical phrases (`greedy…`, `priority`, `matched`, `athlete`, `same`, MediaPipe `Full`).
- Removed bold on the SnatchPhaseBench row in the prior-art comparison table.
- Kept `\textbf{Keywords:}` (standard heading markup, not emphasis).

### Redundancy / flow
- Broke the paper-organization march into three short sentences.
- Compressed ASFormer Results narration toward deltas vs B2 (less isomorphic metric list).
- Related Work: broke long cite-and-contrast sentences; gap list no longer relies on semicolon chains.
- Conclusion rewritten so it does not clone the Abstract inventory.

---

## Repeated expressions removed or reduced

| Pattern | Action |
|---------|--------|
| “artifact / evaluation stack / curated … framework” | Replaced with concrete deliverables |
| Repeated “not a new architecture / protocol not ranking” | Kept once in Abstract; removed from Discussion; Conclusion no longer restates it |
| Symmetric B2/B3 metric paragraphs | ASFormer block rewritten around deltas |
| “This manuscript documents…” | → direct “SnatchPhaseBench comprises…” |
| “In addition,” | Removed |
| Em-dash parentheticals | Rewritten as separate sentences |

---

## Intentional leftovers (not prose AI tells)

| Item | Why kept |
|------|----------|
| Table cells `---` for missing values | Standard numeric-table convention |
| Notation appendix `---` | Same |
| Runtime table ranges `0.46--0.84`, `8.4--15.7` | Compact numeric ranges in tables (not running prose) |
| `\textbf{Keywords:}` | Conventional keyword label |
| Word “artifact(s)” for thesis files / gitignored outputs | Technical noun for files, not brochure framing |
| Figure node bold in landscape TikZ | Visual hierarchy of the proposed box |

---

## Final checklist

- [x] No em dashes (`—`) in prose  
- [x] No `---` / `--` used as prose interrupters (table/notation missing markers and compact table ranges only)  
- [x] No unnecessary bold/italic emphasis in section prose  
- [x] No first-person singular `I`  
- [x] No first-person plural `we` / `our` / `us` in main prose  
- [x] Scientific content (numbers, cites, tables, figures, claims) unchanged  

**Verdict:** voice pass complete for journal submission styling.
