# SnatchPhaseBench — Experiment Matrix

**Parent document:** [`BENCHMARK_PROTOCOL.md`](BENCHMARK_PROTOCOL.md)  
**Status:** Design only — no implementation started

---

## Legend

| Priority | Meaning |
|----------|---------|
| **P0** | Blocks submission |
| **P1** | Strongly recommended |
| **P2** | Optional / appendix |

| Estimate | Person-days (implementation + eval + doc) |
|----------|---------------------------------------------|
| S | 1–3 |
| M | 4–7 |
| L | 8–15 |
| XL | 16+ |

---

## Master matrix

| ID | Experiment | Models | Primary metrics | Figures | Tables | Dependencies | Priority | Est. |
|----|------------|--------|-----------------|---------|--------|--------------|----------|------|
| EXP-ONT | Phase ontology reconciliation | — | — | `fig:phase_illustration` | `tab:phase_taxonomy` | Expert review | **P0** | M |
| EXP-MET | Boundary + segment evaluator | — | boundary MAE, seg-F1 | — | enables all | `segment.py` exists | **P0** | M |
| EXP-B0 | Rule-based knee-angle baseline | B0 | boundary MAE, seg-F1@50, MoF | timeline overlay | `tab:benchmark_comparison`, `tab:boundary_*`, `tab:segment_metrics` | EXP-ONT, EXP-MET | **P0** | M |
| EXP-B1 | Thesis LSTM checkpoint eval | B1 | window P/R/F1 | `fig:confusion_matrix` | `tab:baseline_reproduction`, `tab:baseline_perclass` | **DONE** | — | — |
| EXP-B1-FIG | Baseline figures export | B1 | — | `fig:confusion_matrix`, `fig:training_curves` | — | EXP-B1 | P1 | S |
| EXP-B2-MS | MS-TCN baseline | B2 | boundary MAE, seg-F1@50, edit | `fig:benchmark_comparison` | `tab:benchmark_comparison` | EXP-MET, B0 | **P0** | L |
| EXP-B2-MSPP | MS-TCN++ baseline | B2 | same | same | same | EXP-B2-MS | **P0** | M |
| EXP-B2-ASF | ASFormer baseline | B2 | same | same | same | EXP-MET, B0 | **P0** | L |
| EXP-B2-DIF | DiffAct | B2-ext | same | appendix | `appendix D` | EXP-B2-CORE | P2 | L |
| EXP-B2-GCN | CTR-GCN → TAS | B2-ext | same | appendix | extended table | EXP-B2-MS | P2 | L |
| EXP-B2-C3D | PoseC3D → TAS | B2-ext | same | appendix | extended table | EXP-B2-MS | P2 | L |
| EXP-TRIV | Trivial baselines | majority, persistence, prior | MoF, seg-F1@50 | — | appendix | EXP-MET | P1 | S |
| EXP-SPLIT | LOAO / athlete CV | B0, B2-core | boundary MAE ± CI | split variance | supplementary cols | EXP-B2-CORE | **P0** | L |
| EXP-SEED | Multi-seed runs | B0, B2-core | all primary | error bars | `tab:benchmark_comparison` | EXP-B2-MS | **P0** | M |
| EXP-ABL-W | Window length ablation | MS-TCN | seg-F1, boundary | — | `tab:ablation` | EXP-B2-MS | P1 | M |
| EXP-ABL-V | Visibility features | MS-TCN | same | — | `tab:ablation` | EXP-B2-MS | P1 | S |
| EXP-ABL-ST | MS-TCN stages on/off | MS-TCN | over-segmentation | — | `tab:ablation` | EXP-B2-MS | P1 | S |
| EXP-ROB-POSE | Pose extractor swap | B0, MS-TCN | boundary MAE | robustness bars | appendix | metadata / re-extract | P2 | XL |
| EXP-ROB-CAM | Camera angle strata | B0, B2-core | per-stratum MAE | `fig:error_analysis` | error appendix | metadata | P2 | M |
| EXP-ROB-OCC | Occlusion / catch failures | B0, B2-core | catch/turnover MAE | qualitative | appendix | metadata | P2 | M |
| EXP-IAA | Inter-annotator agreement | — | κ, boundary MAE | — | dataset § | second annotator | P1 | L |
| EXP-RT | Runtime / efficiency | B0, B1, B2-core | params, FPS, train time | optional scatter | `tab:runtime` | B2-core | P1 | M |
| EXP-B3-MB | MotionBERT → TAS | B3 | seg-F1, boundary | appendix | appendix | EXP-B2-MS | P2 | XL |
| EXP-B3-PF | PoseFormer → TAS | B3 | same | appendix | appendix | EXP-B2-MS | P2 | XL |
| EXP-REL | Public release bundle | all | checksums | — | reproducibility appendix | legal | P0 (release) | L |
| EXP-FIG-CLS | Class distribution figure | — | — | `fig:class_distribution` | — | verified counts | P1 | S |
| EXP-FIG-SPL | Split visualization | — | — | `fig:split_visualization` | `tab:split_stats` | split JSON | P1 | S |

---

## Milestone bundles

| Milestone | Experiments | Manuscript gate |
|-----------|-------------|-----------------|
| **M1** Ontology | EXP-ONT | Methods + dataset taxonomy |
| **M2** Credible endpoints | EXP-MET, EXP-B0 | B0 row + boundary tables |
| **M3** Main benchmark | EXP-B2-MS, EXP-B2-MSPP, EXP-B2-ASF, EXP-SEED | `tab:benchmark_comparison` |
| **M4** Uncertainty | EXP-SPLIT | Statistical claims |
| **M5** Polish | EXP-TRIV, EXP-ABL-*, EXP-RT, EXP-B1-FIG | Discussion + appendix |
| **M6** Release | EXP-REL | Zenodo + reproducibility appendix |

---

## Dependency graph (simplified)

```text
EXP-ONT ──→ EXP-B0 ──→ EXP-B2-* ──→ EXP-SPLIT
              ↓              ↓
           EXP-MET ─────────┘
              ↓
           EXP-SEED / EXP-ABL / EXP-RT
EXP-B1 (done)
EXP-IAA (parallel, no model deps)
EXP-REL (parallel, legal deps)
```

---

## Not in v1 scope

- GRU vs LSTM ablation (thesis-era; not benchmark tier)
- OnlineTAS / streaming
- VLM end-to-end
- Clean & jerk dataset extension
- Full HD-GCN family comparison
