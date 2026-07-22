# Manuscript acronym dictionary

**Scope:** `paper/macros/acronyms.tex` + body usage via `\ac{}` / `\acf{}`  
**Date:** 2026-07-22

## Defined and used

| Acronym | Expansion | First-use mechanism | Notes |
|---------|-----------|---------------------|-------|
| TAS | temporal action segmentation | `\acf{TAS}` in Introduction | Primary task acronym |
| MOCAP | motion capture | `\ac{MOCAP}` | Laboratory reference |
| IMU | inertial measurement unit | `\ac{IMU}` | Intro contrast |
| CV | computer vision | `\ac{CV}` | |
| DL | deep learning | `\ac{DL}` | |
| LSTM | long short-term memory | `\ac{LSTM}` | B1 |
| GRU | gated recurrent unit | `\ac{GRU}` | Mentioned as future/planned class |
| TCN | temporal convolutional network | `\ac{TCN}` | |
| STGCN | spatial–temporal graph convolutional network | `\ac{STGCN}` | Intro/methods |
| IoU | intersection over union | `\ac{IoU}` / math | Segment metrics |

## Defined but unused via `\ac{}` (kept for future prose)

| Acronym | Expansion | Recommendation |
|---------|-----------|----------------|
| MAE | mean absolute error | Prefer spelling “boundary MAE” or add `\ac{MAE}` at first Results mention |
| MoF | mean over frames | Prefer “frame accuracy (MoF)” once, then MoF |
| GCN | graph convolutional network | Optional; CTR-GCN often written in full form |
| ML | machine learning | Prefer “machine learning” in leakage sentence |
| RNN | recurrent neural network | Optional |
| IWF | International Weightlifting Federation | Unused; keep or remove at camera-ready |

## Common abbreviations not in `acronyms.tex` (intentional)

| Form | Treatment |
|------|-----------|
| MS-TCN, MS-TCN++, ASFormer, DiffAct | Proper names; not expanded via `\ac` |
| MediaPipe, OpenPose, HRNet, BlazePose | Product/method names |
| CTR-GCN, PoseC3D, NTU RGB+D | Model/dataset names |
| B0–B3 | Benchmark tiers (see terminology dictionary) |
| FPS, GPU, CUDA, VRAM | Standard engineering abbreviations |
| F1, SHA-256 | Standard metrics/checksums |

## Rules

1. Expand with `\acf{}` (or `\ac{}` on first hit) for entries in the acronym package list.
2. Do not redefine the same acronym in prose after `\ac` has introduced it.
3. Do not introduce a new acronym in one section and spell it out later.
4. Before camera-ready, either use or delete unused `\acrodef` entries (MAE, MoF, GCN, ML, RNN, IWF).
