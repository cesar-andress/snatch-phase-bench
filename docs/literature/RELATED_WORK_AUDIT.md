# Related Work audit — SnatchPhaseBench

**Date:** 2026-07-22  
**Manuscript file updated:** `~/papers/snatch-phase-bench/paper/sections/02_related_work.tex`  
**Bibliography updated:** `~/papers/snatch-phase-bench/paper/bibliography.bib`  
**Primary discovery engine:** OpenAlex API (`OPEN_ALEX_KEY`)  
**Auxiliary:** WebSearch / publisher DOIs for metadata confirmation  

**Policy:** Quality over quantity. Every new citation must strengthen the positioning argument.

---

## 1. Search strategy

Lightweight systematic review with iterative saturation:

1. **Title-constrained OpenAlex queries** (preferred over full-text search, which returned noise).
2. **DOI resolution** for known anchors (Cao, Chen, MS-TCN, ASFormer, FineGym, Ding survey).
3. **Backward snowballing** from Ding et al. (TPAMI 2023) referenced works.
4. **Forward snowballing** from Ding survey and MS-TCN (works citing them, 2020–2026).
5. **Domain queries** for snatch/weightlifting CV, markerless sports, MediaPipe, reproducibility, sports video surveys.
6. Stop when additional high-citation hits were either already covered thematically or out of scope (nutrition, influenza “cap-snatching”, generic DL surveys).

OpenAlex authenticated requests succeeded after loading `OPEN_ALEX_KEY` from `~/.bashrc` (unauthenticated quota was exhausted).

---

## 2. Keywords used

| Theme | Example queries / filters |
|-------|---------------------------|
| TAS | `title.search:action segmentation`, `title.search:temporal action segmentation`, ASFormer, MS-TCN |
| Surveys | TAS survey; sports video action recognition survey; human pose estimation survey |
| Snatch / WL | Cao/Chen DOIs; Baumann snatch; Thiele markerless snatch |
| Markerless | `title.search:markerless` + sports/biomechanics |
| MediaPipe | `title.search:MediaPipe` |
| Sports fine-grained | FineGym, MultiSports |
| Reproducibility | reproducibility machine learning; leakage machine learning |
| Boundary TAS | boundary-aware action segmentation; over-segmentation boundaries |

---

## 3. Databases consulted

| Source | Role |
|--------|------|
| **OpenAlex** | Primary discovery, citation counts, DOI metadata, snowballing |
| Publisher DOIs / Crossref-via-OpenAlex | Venue, pages, author strings |
| Existing manuscript + `docs/literature/CAO_CHEN_ALIGNMENT.md` | Ontology provenance |
| Benchmark repo design docs | B2/B3 method placement |

---

## 4. Papers screened

| Stage | Approx. count |
|-------|---------------|
| OpenAlex result rows inspected across curated title searches | **~120** unique rows logged |
| Forward-cite pages (Ding / MS-TCN) inspected | **~40** |
| Backward refs sampled from Ding | **~15** |
| Full-text / abstract relevance decisions | **~55** candidates judged include/exclude |
| Finally cited in manuscript bibliography | **36** |

Saturation: further OpenAlex pages for “weightlifting” and “snatch” were dominated by strength-and-conditioning or non-CV senses of “snatch”; sports-video hits were mostly broadcast event recognition already covered by Wu et al. (2022).

---

## 5. Papers finally cited (36)

### Retained from prior bibliography (corrected where needed)

Cao 2022; Chen 2022; OpenPose; HRNet; BlazePose; Kanko 2021; OpenCap; Harbili 2014; Thiele 2024; ST-GCN; CTR-GCN; NTU RGB+D; PoseC3D; ED-TCN/Lea 2017; MS-TCN; MS-TCN++; ASFormer; DiffAct; Breakfast; 50Salads; GTEA; Kim 2018; FineGym; Shah 2026; SnatchPhaseBench repo.

**Corrections applied:** FineGym authors/pages; ASFormer authors + BMVC DOI; MS-TCN pages/DOI/author order.

### Newly added (11)

| Key | Why it matters for the argument |
|-----|----------------------------------|
| `baumann1988snatch` | Primary historical snatch analysis cited by Chen; grounds phase taxonomy historically |
| `lugaresi2019mediapipe` | Official MediaPipe pipeline paper (complements BlazePose) |
| `chen2020monocular_pose` | CVIU survey of monocular HPE |
| `zheng2023pose_survey` | ACM CSUR HPE survey (recent, comprehensive) |
| `ding2023temporal` | **Essential** TPAMI TAS survey — frames community norms SnatchPhaseBench adapts |
| `wang2020bacs` | Boundary-aware TAS (ECCV) — supports boundary endpoint |
| `ishikawa2021boundary` | Boundary detection to reduce over-segmentation (WACV) |
| `li2021multisports` | Closest large sports spatio-temporal action dataset (ICCV) |
| `wu2022sportsvideo` | IEEE TMM sports video AR survey — maps sports-CV landscape |
| `pineau2021reproducibility` | NeurIPS reproducibility program report |
| `kapoor2023leakage` | Leakage/reproducibility crisis — justifies athlete-disjoint splits |

---

## 6. Newly added references

See table above (11 entries). Net bibliography size: **25 → 36**.

---

## 7. References considered but excluded

| Candidate | Decision | Reason |
|-----------|----------|--------|
| Assembly101 (CVPR 2022) | Exclude | Strong procedural TAS dataset, but redundant with Breakfast/50Salads for our “long procedural vs short lift” contrast |
| C2F-TCN / ICC semi-supervised TAS | Exclude | Method paper; does not change positioning beyond Ding survey + MS-TCN/ASFormer |
| Generic “deep learning survey” OpenAlex hits | Exclude | Irrelevant; full-text search pollution |
| Influenza / microbiology “cap-snatching” | Exclude | Homonym |
| MediaPipe yoga/sign-language application papers | Exclude | Application-only; low relevance to benchmark design |
| AthletePose3D (emerging) | Exclude for now | Pose benchmark for athletes, not snatch phase segmentation; revisit if it becomes a standard citation expectation |
| Deadlift coaching-module CV papers | Exclude | Still no verified peer-reviewed record that strengthens snatch-specific argument; TODO removed rather than citing weak sources |
| Pattern Recognition Letters snatch-theft surveillance | Exclude | Wrong sense of “snatch” |
| Additional barbell load-velocity training papers | Exclude | Biomechanics training literature without CV/segmentation interface |

---

## 8. Literature gap analysis

### 8.1 What gap existed before SnatchPhaseBench?

A structural seam between three literatures:

1. **Biomechanics** defines snatch phases and validates markerless kinematics, but does not release public multi-athlete phase-segmentation leaderboards.
2. **Sports CV** releases datasets/models for fine-grained or localized sports actions (e.g., FineGym, MultiSports), but not Olympic snatch phase labels on fixed pose inputs.
3. **TAS** releases strong segmenters and metrics on long procedural videos whose duration, class count, and order statistics invert those of a 2–6 s ordered lift.

### 8.2 Closest previous datasets

| Dataset | Closeness | Missing for our claim |
|---------|-----------|------------------------|
| FineGym | Fine-grained sports temporal labels | Different sport; RGB; not pose-phase snatch |
| MultiSports | Sports spatio-temporal localization | Multi-person events; not single-lift phases |
| Breakfast / 50Salads / GTEA | Canonical TAS evaluation | Long procedural; not biomechanical phases |
| Thiele et al. trials | Same sport + phase events | Validation study; no public TAS benchmark |
| Chen / Shah barbell sets | Same sport + video | Trajectory/outcome focus; no dense phase labels |

### 8.3 Closest previous benchmarks

| Benchmark / protocol | Closeness | Gap |
|----------------------|-----------|-----|
| MS-TCN / ASFormer eval on Breakfast etc. | Method + metrics | Wrong domain statistics |
| Sports video AR surveys/datasets | Sports video | Rarely phase-boundary biomechanics |
| Markerless vs marker validation protocols | Input validity | Not segmentation leaderboards |

**No published benchmark substantially overlaps SnatchPhaseBench** (athlete-disjoint snatch phase segmentation on fixed MediaPipe pose with TAS + boundary metrics). Closest are FineGym (sports fine-grained) and Thiele (snatch kinematics validity).

### 8.4 What is still missing after all published work?

- Public redistribution of competition video/keypoints (legal).
- Multi-annotator agreement on boundaries.
- LOAO uncertainty as standard reporting.
- Direct public comparison to a fully implemented kinematic rule baseline (B0 frozen exploratory).
- Encoder ablations (CTR-GCN/PoseC3D) under the same protocol.

### 8.5 Papers reviewers may expect

**Essential:** Cao 2022; Chen 2022; Baumann 1988; Thiele 2024; Ding 2023 TAS survey; MS-TCN; ASFormer; OpenPose/MediaPipe; FineGym; Breakfast/50Salads; Kanko/OpenCap validity; Wu 2022 sports survey.

**Strongly expected:** Boundary-aware TAS (BACS / Ishikawa); MultiSports; reproducibility/leakage citations; HPE survey.

**Optional:** DiffAct; PoseC3D/CTR-GCN (kept because Methods mention encoder path).

### 8.6 Weak / obsolete citations in the previous draft

| Item | Action |
|------|--------|
| FineGym wrong author list | **Fixed** |
| ASFormer wrong authors / missing DOI | **Fixed** |
| MS-TCN page range slightly off | **Fixed** |
| Baumann mentioned without cite | **Cited** |
| “Quantitative rankings outside scope until experiments complete” | **Removed** (Results exist; Related Work now points to Results) |
| Deadlift TODO | **Removed** (no verified citation that improves the argument) |

---

## 9. Recommendations for future updates

1. Update `tab_prior_art_comparison.tex` (not modified in this pass) to list B2/B3 and cite Ding/MultiSports/Baumann rows.
2. Revisit AthletePose3D if it becomes a standard sports-pose benchmark citation.
3. Add IAA / legal-release citations when those artifacts exist.
4. Periodically re-run OpenAlex forward cites of Ding 2023 and Thiele 2024 before camera-ready.

---

## 10. Manuscript changes (summary)

**File:** `paper/sections/02_related_work.tex` only (plus `bibliography.bib`).

Major improvements:

- Explicit **“Why a new benchmark?”** paragraph in positioning.
- Integration of **Ding TPAMI survey** as the TAS map.
- **Baumann 1988** as historical primary source behind Chen’s phase figure.
- **Boundary-aware TAS** citations to motivate boundary metrics.
- **Sports CV survey + MultiSports** to separate broadcast sports AR from snatch phases.
- **Pose surveys + MediaPipe** for input stack completeness.
- **Reproducibility + leakage** citations to justify athlete-disjoint evaluation.
- Removed stale TODO and “experiments not complete” wording.

### Quality check

| Check | Status |
|-------|--------|
| Every citation in `.bib` | Pass (36/36) |
| Every `.bib` entry cited | Pass |
| Duplicate keys | None |
| Terminology (TAS, B2/B3, seven-class) | Consistent with Methods |
| Narrative leads to SnatchPhaseBench | Yes — ends with explicit necessity argument |

### Publication-readiness of Related Work alone

**Yes, with one residual production note:** `tab_prior_art_comparison` still says “LSTM + planned TAS/B0” and should be refreshed in a separate edit. The prose of §2 is now suitable for Q1 review on literature positioning.

---

## Appendix A — Example OpenAlex query log (selected)

| Query | Filter / sort | Year window | Decision pattern |
|-------|---------------|-------------|------------------|
| `title.search:action segmentation` | cited_by_count desc | 2017–2026 | Include MS-TCN++, BACS, Ishikawa, Ding; exclude weak application TAS |
| `title.search:ASFormer` | — | — | Include Yi et al. |
| `title.search:FineGym` | — | — | Include Shao et al. |
| `title.search:MultiSports` | — | — | Include Li et al. ICCV |
| `title.search:MediaPipe` | cited_by_count | 2019–2026 | Include Lugaresi; exclude yoga/sign apps |
| `title.search:markerless` | cited_by_count | 2018–2026 | Keep Kanko/OpenCap/Thiele already in; exclude animal tracking |
| DOI `10.1109/TPAMI.2023.3327284` | — | — | Include Ding survey |
| DOI `10.1123/ijsb.4.1.68` | — | — | Include Baumann |
| Cites Ding / MS-TCN | 2020–2026 | — | Mostly redundant method papers; exclude |

Full machine-readable scrape snapshot (partial): `/tmp/oa_curated.json` (local, not committed).

---

*End of Related Work audit.*
