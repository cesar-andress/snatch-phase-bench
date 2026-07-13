# Author clarifications — phase taxonomy and dataset construction

**Source:** Direct clarifications from the original MSc thesis author (Adrián Cardona Ruiz), together with the original checkpoint and the literature that motivated the phase taxonomy.  
**Integrated:** 2026-07-13  
**Status:** Canonical reference for dataset construction decisions confirmed after Phase 2 reproduction.

Do **not** treat claims here as verified unless they appear in this document or in cited literature. Experimental results are unchanged.

---

## Phase taxonomy

### Coaching vs. computer-vision conventions

Weightlifting coaching traditionally describes the snatch pull using **three or four pulling phases** (e.g., first pull, transition/scoop, second pull, and optionally a distinct turnover or receiving phase depending on coaching model).

Computer-vision literature on snatch analysis more commonly adopts a **six-phase** decomposition driven by barbell trajectory and lower-limb joint-angle events. Cao et al. (2022) define six phases (M1–M6) from start position through squat receipt, using barbell kinematics and knee/hip/ankle angles as boundary markers (Applied Sciences, 12(19):9679). Chen et al. (2022) situate snatch analysis in the same competition-video, barbell-trajectory tradition used for automated performance evaluation (ICAAI 2022).

### Seven supervised phases in SnatchPhaseBench

During dataset construction, the author followed the **six-phase CV decomposition** inspired by Cao et al. (2022) and Chen et al. (2022), and added an additional **Setup** phase preceding the first pull. The benchmark therefore uses **seven** supervised phase labels:

| ID | Phase name |
|----|------------|
| 1 | Setup |
| 2 | First Pull |
| 3 | Transition |
| 4 | Second Pull |
| 5 | Turnover |
| 6 | Catch |
| 7 | Recovery |

(`unlabeled` remains an annotation utility class excluded at window centers during training.)

### Rationale for Setup as an active biomechanical phase

Frames before barbell separation are labelled **Setup** rather than `unlabeled` because the lifter is in an **active coached start position**: grip is established, the body is braced, and postural alignment is maintained before the first pull begins. This interval is a distinct technical phase in coaching practice, not passive pre-roll footage. It precedes the first-pull onset defined in kinematic studies (e.g., Cao et al.'s M1 boundary at first maximal knee extension).

### Rationale for separating Turnover and Catch

**Turnover** and **Catch** were intentionally kept as separate labels. In the six-phase barbell-kinematics model of Cao et al. (2022), late-lift events span maximal bar height, peak downward bar velocity, and descent into the receiving squat (M4–M6). Separating turnover (bar flight and arm rotation under the bar) from catch (receipt and fixation overhead before recovery) yields finer temporal resolution than collapsing both into a single class, and aligns with coaching vocabulary that treats receiving as distinct from the aerial turnover phase. Biomechanical validation work likewise treats turnover as ending once the bar is stabilized in the overhead position, before the recovery stand-up (Thiele et al., 2024).

---

## Phase boundaries

Phase boundaries were **manually annotated frame-by-frame** by identifying **visually identifiable biomechanical transition events** (e.g., onset of bar separation, knee-angle reversals, bar path inflection, overhead fixation).

**Recovery** ends only after **complete extension of hips and knees** with the **bar stabilized overhead**—not merely at initial receipt in the squat.

---

## Annotation protocol

| Aspect | Decision |
|--------|----------|
| Annotators | **One expert annotator** (thesis author) |
| Method | **Manual frame-by-frame** labelling |
| Criterion | **Visual identification** of biomechanical transition events |
| Consistency | **Prioritised across athletes** over clip-local optima |
| Ambiguous transitions | Select the **closest visually consistent frame** |
| Future work | **Inter-annotator agreement** study on a held-out subset |

Segment labels (`master_segment_labels.csv`) are derived from the frame labels for evaluation convenience.

---

## Frame count reconciliation

| Source | Row count | Status |
|--------|-----------|--------|
| Earlier export / thesis draft | 37,125 | Superseded |
| Corrected `master_frame_labels.csv` | **35,825** | **Canonical** |

The larger file contained **duplicated labels**, **filename inconsistencies**, and **annotation errors**. Examples include duplicated filenames differing only by weight-class spelling (e.g., `-88k` vs `-88kg`), which produced redundant or conflicting rows.

The **corrected dataset** (35,825 rows, 208 videos, no duplicate `(video, frame)` keys) is the **canonical benchmark version**. Rebuilt tensors and checkpoint evaluation use this file exclusively.

---

## Dataset provenance

| Item | Detail |
|------|--------|
| Clips | **208** snatch attempts |
| Extraction | Manually extracted from **international weightlifting competition broadcasts** |
| Source channel | **Weightlifting House** YouTube videos |
| Trimming | Clips **manually trimmed** to attempt boundaries before annotation |
| Redistribution | **Rights under evaluation** — public video release not yet cleared |

---

## Pose extraction

| Setting | Value |
|---------|-------|
| Library | **MediaPipe 0.10.30** |
| Model | **Full** (`pose_landmarker_full.task`) |
| Output | 33 landmarks × (x, y, z) per frame |

Pose extraction was run once per trimmed clip; keypoint CSVs bundled with the benchmark are the fixed Stage-1 input for benchmark v1.

---

## Related documents

- [`../dataset/dataset.md`](../dataset/dataset.md) — verified counts and file layout
- [`../research_design.md`](../research_design.md) — scientific framing with literature vs. construction vs. post-reproduction clarifications
- [`REMAINING_BLOCKERS.md`](REMAINING_BLOCKERS.md) — open items after this integration
- [`CHECKPOINT_VALIDATION.md`](CHECKPOINT_VALIDATION.md) — baseline metrics unchanged on canonical labels
