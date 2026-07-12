# Publication strategy

Distilled from [`SnatchPhaseBench_Literature_Foundation.md`](../../../SnatchPhaseBench_Literature_Foundation.md) Part 7.

**Manuscript:** `paper/main.tex`  
**Reviewer risks:** [`paper/REVIEWER_CHECKLIST.md`](paper/REVIEWER_CHECKLIST.md)

---

## 1. What the contribution actually is

Ranked by defensibility (do not reorder for marketing):

| Rank | Contribution | Claim in paper? |
|------|--------------|-----------------|
| 1 | **Dataset** — annotated snatch videos, athlete metadata, splits | Yes — primary |
| 2 | **Benchmark** — protocol, baselines, eval code | Yes — primary |
| 3 | **Domain formalization** — short-horizon TAS + boundary-ms metrics | Yes — secondary |
| 4 | **Software** — reproducible toolkit | Yes — supporting |
| 5 | **New model / architecture** | **No** |

---

## 2. Story sentence (use in abstract and conclusion)

> We introduce the first reproducible, athlete-disjoint benchmark for markerless phase segmentation of the Olympic snatch, casting a biomechanically grounded task as short-horizon temporal action segmentation, and we show—with boundary-level, millisecond-scale evaluation against kinematic events—where learned segmenters do and do not improve over the biomechanical heuristic the field currently uses.

Adapt only if experiments contradict; never promise superiority in advance.

---

## 3. Venue fit (honest assessment)

| Venue | Fit | Notes |
|-------|-----|-------|
| **Sensors** | **Best fit** | Benchmark/dataset friendly; sports-CV receptive |
| **Biomedical Signal Processing and Control** | **Best fit** | Signal + biomechanics framing |
| **Sports Biomechanics** | Stretch | Strong if kinematics/heuristic comparison foregrounded; weaker if DL-heavy |
| **IEEE JBHI** | Stretch | Needs clinical/health hook (injury risk, coaching decision support) |
| **Computer Methods and Programs in Biomedicine** | Stretch | Needs software-methods or clinical angle |
| **Pattern Recognition** | **Poor fit** | Expects methodological novelty; niche benchmark likely seen as incremental |

**Primary targets:** Sensors, BSPC.  
**Do not lead with Pattern Recognition** without a genuine methods contribution.

---

## 4. Release strategy

| Artifact | Plan | Status |
|----------|------|--------|
| Code | Public GitHub (current) | Active |
| Splits | Ship `athlete_split.json` with release | Available in snapshot |
| Eval script | Package `snatch_phase_bench.evaluation` | Implemented |
| Processed tensors | Rebuild from keypoints + annotations | Verified exact |
| Raw videos | Not in current export | **Legal review required** |
| Athlete pseudonyms | Required before public dataset | TODO |
| Zenodo DOI | On public release milestone | TODO |
| Checkpoint | `best_model.pt` when validated | Blocked (LFS) |

A benchmark that is not fully reproducible is not a benchmark — release checklist is submission-critical.

---

## 5. Submission readiness gates

- [ ] G0: Checkpoint validated
- [ ] G1: Phase ontology reconciled
- [ ] G2: B0 + boundary metrics reported
- [ ] G3: MS-TCN / ASFormer baselines complete
- [ ] Essential citations verified in BibTeX
- [ ] Related Work prose complete (not outline)
- [ ] Results tables populated from committed experiments only
- [ ] Reviewer checklist: all P0 items mitigated or honestly conceded
- [ ] Legal clearance for video release or documented restriction

---

## 6. What not to do

- Bolt on VLMs or “novel modules” to inflate perceived novelty
- Claim state-of-the-art without segment-level and boundary evidence
- Submit to methods venues with dataset-only contribution
- Hide rule-based baseline results if learning does not win

---

## 7. Related documents

- [`../research_design.md`](../research_design.md)
- [`../benchmark/BENCHMARK_PLAN.md`](../benchmark/BENCHMARK_PLAN.md)
- [`../paper/PAPER_TODO.md`](../paper/PAPER_TODO.md)
- [`../SCIENTIFIC_WORKFLOW.md`](../SCIENTIFIC_WORKFLOW.md)
