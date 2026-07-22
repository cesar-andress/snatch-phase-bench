# Manuscript terminology dictionary

**Scope:** SnatchPhaseBench LaTeX manuscript (`~/papers/snatch-phase-bench/paper/`)  
**Date:** 2026-07-22  
**Policy:** Prefer the canonical form in the left column in all new prose.

| Canonical term | Allowed variants | Avoid |
|----------------|------------------|-------|
| SnatchPhaseBench | — | Snatch Phase Bench, SPB (except code paths) |
| benchmark | SnatchPhaseBench when naming the artifact | challenge, contest |
| dataset | SnatchPhaseBench dataset | corpus (unless citing external corpora) |
| baseline | historical / frozen baseline; B0/B1/B2/B3 with definition | model (when meaning baseline tier) |
| B0 | exploratory knee-angle reference | “rule baseline” without B0 |
| B1 | frozen LSTM / historical window baseline | “thesis model” alone |
| B2 | MS-TCN (frozen) | “M3” in reader-facing prose (OK in protocol docs) |
| B3 | ASFormer (frozen) | — |
| phase | seven-class phase; named phases in `\texttt{}` | stage (except Cao M1–M6) |
| segment | contiguous phase interval | clip (unless trimmed recognition) |
| boundary | phase transition / boundary timing | cut, breakpoint |
| frame | video frame index | timestep (OK in equations) |
| transition | (1) phase name `transition`; (2) phase change event | — (disambiguate in context) |
| athlete | — | subject (except TAS literature) |
| video / attempt | snatch attempt keyed by `video_relpath` | trial (OK if equated once) |
| sequence | pose sequence / frame sequence | stream (except MediaPipe docs) |
| MediaPipe | MediaPipe Pose Landmarker; version when relevant | BlazePose alone when MediaPipe CSVs are used |
| MS-TCN | — | MSTCN, ms-tcn in prose |
| ASFormer | — | Asformer |
| LSTM | historical baseline | RNN (unless discussing class) |
| window | sliding window ($W{=}31$) | snippet |
| athlete-disjoint | athlete-level split | patient-level, subject-disjoint (unless TAS cite) |
| segment F1@50 | segmental F1 at IoU $0.50$ | F1 alone |
| boundary MAE | MAE in **frames** | MAE in ms unless FPS verified |
| seven-class taxonomy | seven supervised phases (+ unlabeled) | seven-phase (OK as synonym; prefer seven-class in Methods) |

## Tier shorthand (must stay consistent)

| Tier | Meaning |
|------|---------|
| B0 | Exploratory knee-angle reference (not implemented) |
| B1 | Frozen LSTM window classifier (thesis reproduction) |
| B2 | Frozen MS-TCN dense segmenter |
| B3 | Frozen ASFormer dense segmenter |
