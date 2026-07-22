# Competitor benchmark audit — SnatchPhaseBench

**Date:** 2026-07-22  
**Primary engine:** OpenAlex (`OPEN_ALEX_KEY`)  
**Auxiliary:** DOI resolution via OpenAlex; Crossref not required for final table rows  
**Policy:** No fabricated datasets/DOIs; novelty claims scoped to literature search evidence  
**Manuscript touch:** `sections/02_related_work.tex` §Research gap wording strengthened (no experimental changes)

---

## 1. Complete search strategy

1. **Theme queries** (OpenAlex `search` / `title.search` + year filters 2015–2026).  
2. **Title-constrained dataset lookups** for named corpora (FineGym, FineDiving, Diving48, HAA500, SportsHHI, MultiSports, PoseTrack, …).  
3. **DOI resolve** for known anchors already in the bibliography.  
4. **Domain filter** for snatch / Olympic weightlifting / barbell trajectory / markerless snatch.  
5. **Noise control:** discard medical “cap-snatching,” generic metaverse/ML surveys, and non-CV weightlifting training papers.  
6. **Saturation:** additional weightlifting/snatch pages were dominated by strength-and-conditioning or virology senses of “snatch”; no additional *public pose-phase TAS* snatch benchmark appeared.

---

## 2. OpenAlex queries used (representative)

| ID | Query |
|----|--------|
| Q1 | `search=weightlifting dataset OR snatch dataset OR "clean and jerk" dataset` + `publication_year:2015-2026` |
| Q2 | `filter=title.search:snatch,publication_year:2018-2026` |
| Q3 | `search=sports action segmentation dataset benchmark` + year filter |
| Q4 | `search=fine-grained sports dataset OR FineGym OR FineDiving OR Diving48` |
| Q5 | `search=temporal action segmentation benchmark dataset` |
| Q6 | `search=human pose sports dataset markerless weightlifting OR gymnastics` |
| Q7 | `filter=title.search:FineGym` / `FineDiving` / `Diving48` / `HAA500` / `SportsHHI` / `MultiSports` / `PoseTrack` |
| Q8 | `filter=title.search:sports dataset OR sports benchmark,publication_year:2022-2026` |
| Q9 | DOI resolves: FineGym, FineDiving, MultiSports, Wu TMM survey, Ding TPAMI survey, Cao/Chen/Thiele snatch papers, HAA500, SportsHHI, PoseTrack, RESOUND/Diving48 paper |

---

## 3. Candidate datasets examined

### A. Explicitly requested list

| Dataset | Examined? | OpenAlex / literature status |
|---------|-----------|------------------------------|
| FineGym | Yes | CVPR 2020; hierarchical gymnastics actions; public |
| FineDiving | Yes | CVPR 2022; diving AQA / procedures; public |
| Diving48 | Yes | Introduced via RESOUND (ECCV 2018 lineage); diving clip classification; not phase TAS |
| Gym99 | Yes | Appears as FineGym-related fine-grained gym setting in follow-on papers; not a snatch phase benchmark |
| SportsHHI | Yes | CVPR 2024; human–human interaction detection in sports; public paper/dataset claim |
| HAA500 | Yes | ICCV 2021; atomic human-centric actions; not weightlifting phases |
| Kinetics | Yes (scope check) | Large clip AR; no snatch phase protocol |
| Something-Something | Yes (scope check) | Object-interaction AR; out of scope |
| Penn Action | Yes | Pose-based action recognition; sports actions but not Olympic snatch phase TAS |
| Human3.6M | Yes | Marker-based 3D pose lab corpus; not sports phase TAS |
| COCO / MPII | Yes | Still-image pose; rejected for temporal segmentation comparison |
| PoseTrack | Yes | Multi-person pose tracking benchmark; not phase labels |
| Olympic weightlifting datasets | Yes | Cao/Chen/Thiele/Shah lines: kinematics, trajectories, or validation—**no public snatch phase TAS benchmark found** |
| Biomechanics public video phase sets | Yes | Thiele et al. (2024) snatch markerless validation; not a shared ML benchmark release |

### B. Additional candidates from 2022+ “sports benchmark” title search

SportQA, FSBench, SCBench, SPORTU, GOAL, camera-calibration sports protocol, yoga/dance posture benchmark—**rejected** as LLM/QA, figure-skating understanding, or posture classification rather than snatch phase TAS.

### C. Canonical TAS corpora (overlap via metrics, not sport)

50Salads, Breakfast, GTEA—long procedural TAS benchmarks; used for metric norms, not weightlifting.

---

## 4. Final comparison table (realistic overlap only)

Legend: ✓ = yes / present; ∼ = partial; — = no / not applicable.

| Dataset | Sport | Markerless video | Olympic WL | Snatch-specific | Frame-level phase labels | Temporal seg. benchmark | Public protocol | Std. metrics | Public availability |
|---------|-------|------------------|------------|-----------------|--------------------------|-------------------------|-----------------|--------------|---------------------|
| **SnatchPhaseBench** | Olympic snatch | ✓ (MediaPipe from RGB) | ✓ | ✓ | ✓ (7 phases + unlabeled) | ✓ (dense TAS + boundary MAE) | ✓ (locked B1–B3) | ✓ (frame/segment/boundary) | Labels/keypoints/code; raw video pending |
| FineGym | Gymnastics | ✓ RGB | — | — | ∼ hierarchical actions/events | ∼ fine-grained understanding | ✓ | ✓ recognition | ✓ |
| FineDiving | Diving | ✓ RGB | — | — | ∼ procedure / AQA stages | ∼ procedure-aware AQA | ✓ | ✓ AQA | ✓ |
| MultiSports | Multi-person sports | ✓ RGB | — | — | Spatio-temporal action tubes | Localization, not phase TAS | ✓ | ✓ detection | ✓ |
| SportsHHI | Multi-person sports | ✓ RGB | — | — | Human–human interactions | Interaction detection | ✓ (paper) | Detection | ✓ (paper) |
| HAA500 | Atomic actions (many) | ✓ RGB | — | — | Atomic action classes | Clip/atomic AR | ✓ | Recognition | ✓ |
| Diving48 | Diving | ✓ RGB | — | — | Clip class labels | Clip AR (bias study) | ✓ | Recognition | ✓ |
| 50Salads / Breakfast / GTEA | Cooking / ADL | ✓ RGB (+sensors) | — | — | ✓ frame actions | ✓ canonical TAS | ✓ | MoF / edit / F1@τ | ✓ |
| Kim & Kim (Sensors 2018) | Sports motions | Wearable IMU | — | — | Boundary states | Online segmentation | Paper | Detection | Paper (not pose TAS) |
| Thiele et al. 2024 | Snatch | Marker + markerless | ✓ | ✓ | Knee-event phases (validation) | — (agreement study) | — | Kinematic error | No public TAS split |
| Chen et al. 2022 / Shah et al. 2026 | Snatch / barbell | ✓ RGB | ✓ | ✓ | — (trajectory / score) | — | — | Classification / tracking | No phase TAS release |
| PoseTrack / Human3.6M / COCO / MPII | General | Mix | — | — | Pose keypoints | Pose / tracking | ✓ | Pose metrics | ✓ (wrong task) |
| Kinetics / SSv2 | General | ✓ RGB | — | — | Clip labels | Clip AR | ✓ | Top-1/5 | ✓ (wrong task) |

**Only rows above the dashed conceptual cut (sports fine-grained + TAS + snatch lines) are “realistic competitors.”** Image/pose/tracking corpora are listed to document explicit rejection.

---

## 5. Competitor benchmarks accepted (partial overlap)

These are **accepted as neighbouring public resources** the manuscript must acknowledge:

1. **FineGym** — fine-grained sports video; hierarchical gymnastic actions.  
2. **FineDiving** — fine-grained sports procedures / AQA.  
3. **MultiSports** — sports spatio-temporal action localization.  
4. **Canonical TAS sets** (50Salads, Breakfast, GTEA) — metric and method transfer.  
5. **HAA500 / SportsHHI / Diving48** — sports or atomic-action video resources (weaker overlap).  
6. **Snatch biomechanics / barbell-CV papers** (Cao, Chen, Thiele, Shah) — domain semantics without a shared pose-phase TAS protocol.

None of (1)–(6) currently provides the full SnatchPhaseBench combination.

---

## 6. Competitor benchmarks rejected (as comparable snatch phase TAS benchmarks)

| Candidate | Reason for rejection as *comparable* benchmark |
|-----------|--------------------------------------------------|
| Kinetics, Something-Something | Clip AR; no snatch phases |
| COCO, MPII | Still-image detection/pose |
| Human3.6M | Lab 3D pose; not sports phase TAS |
| PoseTrack | Pose tracking, not phase segmentation |
| Penn Action | Pose AR actions; not Olympic snatch phase ontology |
| SportQA / FSBench / SCBench / SPORTU | LLM/video-QA sports understanding |
| Gym99 (as standalone) | FineGym-related gym setting; not snatch |
| Cap-snatching virology hits | Homonym noise |
| Strength-training RCTs with “weightlifting” in title | No CV benchmark |

---

## 7. Recommended wording for novelty claims

**Prefer:**

> To the best of our OpenAlex-backed literature review, we did not identify a publicly available benchmark that jointly provides athlete-disjoint snatch phase labels on markerless pose sequences, locked dense TAS baselines, and boundary-centric timing metrics reported together with community segment scores.

**Also prefer:**

> Closest neighbours (FineGym, FineDiving, MultiSports, canonical TAS corpora, and snatch biomechanics/barbell-CV studies) each omit at least one of: Olympic snatch phase semantics, pose-sequence TAS evaluation, or a shared reproducible protocol.

**Avoid:**

- “first ever,” “unique,” “no previous work,” “no benchmarks exist.”

**Manuscript status:** §Research gap in `02_related_work.tex` updated to this wording (2026-07-22).

---

## 8. Does current Related Work accurately reflect the state of the art?

**Mostly yes**, after the 2026 Related Work rewrite and this audit’s gap tightening.

| Aspect | Assessment |
|--------|------------|
| Acknowledges FineGym / FineDiving / MultiSports / TAS corpora | Yes |
| Avoids “no sports datasets exist” | Yes |
| States remaining gap as a *combination* | Yes (updated) |
| Mentions HAA500 / SportsHHI / Diving48 in main text | Optional; covered here to avoid padding |
| Overclaims snatch exclusivity beyond evidence | No |

---

## 9. Final verdict

### Does the manuscript adequately justify the need for SnatchPhaseBench?

**Yes.**

Justification is strongest when framed as a **missing intersection**, not as absolute uniqueness:

- Olympic weightlifting / snatch **phase** semantics;  
- markerless **pose-sequence** inputs;  
- **frame-level** phase labels;  
- athlete-disjoint **benchmark protocol** with locked dense TAS baselines;  
- **boundary timing** metrics co-reported with segment scores.

Public competitors cover pieces of this stack (fine-grained sports RGB, multi-person localization, procedural TAS, or snatch kinematics/trajectories) but, on the evidence of this audit, **not the full combination**.

---

## 10. What SnatchPhaseBench still must not overclaim

- Raw competition video is **not** fully public yet (pending legal review).  
- IAA for boundaries is **not** yet measured.  
- Scale (208 attempts / 70 athletes) is modest vs Kinetics-scale corpora.  
- Future discovery of a public snatch phase TAS release would require updating this audit.

---

*End of BENCHMARK_COMPETITOR_AUDIT.md*
