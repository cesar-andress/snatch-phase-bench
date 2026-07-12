# Related Work revision log (2026-07-13)

Manuscript changes live in `~/papers/snatch-phase-bench/paper/` (outside Git).

## Summary

Section 2 was rewritten as a critical, publication-oriented Related Work with verified citations, a prior-art comparison table, and a TikZ conceptual figure.

## Files changed (manuscript)

| File | Change |
|------|--------|
| `sections/02_related_work.tex` | Full rewrite (§2.1–§2.7) |
| `sections/01_introduction.tex` | Citations aligned with §2; organization paragraph updated |
| `sections/07_discussion.tex` | Cross-reference to `tab:prior_art_comparison` |
| `bibliography.bib` | Replaced `@misc{todo_*}` with 22 verified entries |
| `tables/tab_prior_art_comparison.tex` | **New** — prior-art comparison (verified rows only) |
| `figures/fig_related_landscape.tex` | **New** — TikZ conceptual pipeline figure |
| `preamble.tex` | Added TikZ libraries |

## Citations added (verified)

MS-TCN, MS-TCN++, ASFormer, DiffAct, ED-TCN, ST-GCN, CTR-GCN, PoseC3D, NTU RGB+D, OpenPose, HRNet, BlazePose, Kanko et al., OpenCap, Harbili & Alptekin, Thiele et al., Kim & Kim (wearable), FineGym, Shah et al. (barbell trajectory), Breakfast, 50Salads, GTEA, SnatchPhaseBench repo.

## Remaining TODOs

| ID | Item |
|----|------|
| LIT-DEADLIFT | Peer-reviewed deadlift / multi-lift CV papers — bibliographic verification pending |
| LIT-OPENCAP-EXT | Optional: PoseBench3D, systematic Theia3D review (not yet in bib) |
| LIT-07 | Benchmarks & reproducibility subsection (PoseBench3D) — deferred |
| EXP-12 | Phase ontology reconciliation (5 vs 7 phases) — must not overclaim in prose |
| SHAH-2026 | Confirm final publisher metadata for Shah et al. SN Computer Science 2026 |

## Compile status

`make` → **28 pages**, bibliography populated, minor table overfull (<20pt) in `tab:prior_art_comparison`.

## Unresolved literature gaps

- No public snatch phase-segmentation benchmark with athlete-disjoint splits (the gap SnatchPhaseBench targets)
- Rule-based knee-angle baseline (B0) not yet implemented in code
- Direct numeric comparison with prior weightlifting papers impossible (different tasks/metrics)
