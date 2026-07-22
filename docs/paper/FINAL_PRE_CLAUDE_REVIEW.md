# Final pre-Claude editorial review

**Date:** 2026-07-22  
**Role:** Senior co-author final pass (editorial + publication readiness).  
**Constraint:** No new experiments, statistics, annotations, or legal clearance work.  
**Manuscript path:** `~/papers/snatch-phase-bench/paper/` (outside software Git); sync notes below.

---

## 1. Issues corrected

### Objective (Priority 1)

- Removed duplicate **Frame MoF** column (identical to frame macro-F1) from `tab_benchmark_comparison`.
- Removed **empty future-model / B0 rows** from comparison, segment, boundary, and runtime tables.
- Dropped redundant Params column from comparison (runtime table keeps complexity).
- Dropped redundant “Test windows” triple row from `tab_baseline_reproduction`.
- Fixed notation: $\mathrm{MAE}_{\mathrm{bnd}}$ defined in **frames** (was ms).
- Harmonized phase names in per-class recall tables to `\texttt{snake_case}`.
- Shortened figure/table captions; removed production jargon from captions.
- Wired `\Cref` **before** floats for Results figures/tables and `tab:dataset_stats`, `tab:lstm_hyperparams`, `tab:segment_metrics`, `tab:boundary_metrics`, `tab:runtime`.
- Deduplicated Cao/Chen history: Related Work points to Dataset; Methods annotation cross-refs Dataset; Protocol no longer retells ontology origin.
- Collapsed novelty disclaimer to Abstract + Conclusion (removed Related Work “not an architecture paper” / “order of defensibility” block).
- Related Work now **bridges into Dataset**.
- Threats (Discussion) vs Limitations: complementary (validity framing vs release/IAA/metadata/eval-design bullets).
- Conclusion rewritten from **empirical pattern**, not Abstract inventory.
- Discussion interprets frame-vs-segment/boundary pattern; no longer restarts full Results dump.
- Trimmed “frozen/canonical/verified/This section” drumbeat in Intro/Methods/Protocol/Results.

### Positioning (Priority 2)

- Abstract/Intro: contribution = protocol + locked baselines; **raw video pending** stated honestly; removed “Public release status” as a contribution bullet.
- Softened uniqueness claim (“To our knowledge…”).
- B2/B3 framed as protocol baselines; deltas labeled descriptive / no athlete-level tests (existing limitation).
- Benchmark (not ASFormer) kept as protagonist; ASFormer figures are illustrative under the protocol.

### Readability (Priority 3)

- Broke B2/B3 Results symmetry (B3 reported via deltas + cites).
- Shortened Methods model subsections and Protocol config wall.
- Compressed Discussion/Limitations/Conclusion.

---

## 2. Issues intentionally left unchanged

| Issue | Why left |
|-------|----------|
| No public raw video / pending legal review | Cannot complete before submission; now scoped + limited honestly |
| No IAA | Would require new annotation; acknowledged in Limitations |
| No athlete-level significance / LOAO | Would be new analysis; stated as descriptive seed summaries + limitation |
| No FPS → no ms timing | Metadata absent; frames endpoint retained + explained |
| No B0 implementation / no MS-TCN++ | Future tiers; removed from tables, kept as limitation |
| Training-curve / single-seed confusion figures | Existing assets; cited; useful enough without regeneration |
| 150 dpi PNGs | Regeneration is tooling polish; not blocking if content is correct |
| Full Related Work survey depth | Already adequate; only trimmed positioning |

---

## 3. Reviewer criticisms now addressed (with existing material)

- Misleading empty leaderboard rows / duplicate MoF  
- Incomparable LSTM columns presented as peer dense metrics (now footnote-only Acc + window F1)  
- Contribution inflation (“pending release” as a contribution)  
- Repeated novelty / Cao–Chen / B0 sermons  
- Discussion that only reprints Results  
- Conclusion = second Abstract  
- Related Work pointing past Dataset  
- Notation units inconsistency (ms vs frames)  
- Orphan Results floats (missing `\Cref`)  
- Over-selling architecture ranking (now explicitly descriptive)

---

## 4. Reviewer criticisms that still require future work

- Public redistribution of competition video  
- Inter-annotator agreement on boundaries  
- Athlete-level uncertainty / multi-split  
- Native FPS and demographics  
- Quantified MediaPipe error on this footage  
- Implemented B0 or additional TAS models  

These remain in Limitations without unsupported promises.

---

## 5. Remaining risks before submission

1. Skeptical reviewers may still reject “benchmark” framing without public video—even with the narrowed release statement.  
2. Boundary MAE as a highlighted endpoint without IAA remains a soft spot (mitigated by honest limitation, not eliminated).  
3. Single fixed split + three seeds will be questioned if anyone reads B2/B3 as a strong architecture claim (text now discourages that reading).  
4. LaTeX production risks remain (e.g. `\repo`/`\path` in moving arguments from earlier audits)—compile locally before upload.  
5. External `\repo{...}` pointers assume reviewers accept supplemental docs.

---

## 6. Overall submission readiness

**58 / 100** (up from internal No-Go ~28 on claim hygiene; still below “comfortable submit” for a public-benchmark venue).

Scientific numbers for B1/B2/B3 were **not** altered.

---

## 7. Final recommendation

**READY FOR CLAUDE REVIEW**

Not “ready for journal upload tomorrow” without co-author sign-off on release wording, but ready for an external editorial/LLM review pass on the strengthened manuscript.

---

### Manuscript sync (outside software Git)

Edited under `~/papers/snatch-phase-bench/paper/`: Abstract, §§1–9, key tables/figures, notation appendix.  
This file records the co-author pass; commit lives in `snatch-phase-bench` docs only.

---

*End of final pre-Claude review.*
