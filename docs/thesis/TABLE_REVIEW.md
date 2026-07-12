# Table review — thesis to journal

| Thesis table | Approx. page | Classification | Journal target | Notes |
|--------------|--------------|----------------|----------------|-------|
| Table 4.4.1 — Resumen general del dataset | 15 | **Update** | `tab:dataset_stats` | Merge; add FPS/resolution/license rows still pending |
| Table 4.4.2 — Distribución frame labels | 15 | **Update** | `tab:class_distribution` or appendix | Frame-level vs window-level; thesis frame counts differ from audit — resolve |
| Table 4.4.3 — Distribución ventanas (meta) | 15–16 | **Reuse** | `tab:class_distribution` | **Verified** — matches rebuild |
| Table 6.6.1 — División por atleta (49/10/11) | 19 | **Reuse** | `tab:split_stats` | **Verified** |
| Table 6.6.2 — Fases por subconjunto | 19 | **Update** | **New:** `tab:split_phase_distribution` (proposed) | High value; not yet in manuscript |
| Table 6.7.1 / 6.7 — Configuración LSTM | 20 | **Reuse** | `tab:lstm_hyperparams` | **Verified** |
| Table 7.1.1 — Métricas globales | 22 | **Replace** | `tab:baseline_reproduction` | Pending checkpoint; thesis values in column “Thesis artifact” only after gate |
| Table 7.2.1 — Mejor resultado validación | 22 | **Update** | App. C / training caption | Epoch 5 metrics; not standalone table yet |
| Table 7.3.1 — Resultados por fase test | 24 | **Replace** | `tab:baseline_perclass` | Populate after validation |
| Table 7.6.1 — Objetivos cumplidos | 30 | **Discard** | — | TFM administrative |
| Table 7.6.1 — Futuras líneas de trabajo | 33 | **Replace** | Benchmark plan / §7 future | Map to `BENCHMARK_PLAN.md`, not copied |

---

## Journal tables not in thesis (planned)

| Table | Status | Source |
|-------|--------|--------|
| `tab:benchmark_comparison` | Placeholder | Phase 3 |
| `tab:segment_metrics` | Placeholder | Phase 3 |
| `tab:boundary_metrics` | Placeholder | Boundary implementation |
| `tab:boundary_per_transition` | Placeholder | Phase 3 |
| `tab:ablation` | Placeholder | Ablation study |
| `tab:runtime` | Placeholder | Runtime logs |
| `tab:notation` | **Reuse** | App. notation (new vs thesis) |
| `tab:repro_checklist` | **Reuse** | App. B (new vs thesis) |

---

## Recommended new table from thesis

**`tab:split_phase_distribution`** — copy structure from thesis Table 6.6.2 (train/val/test × seven phases). Scientific impact: explains why transition has only 117 test windows and supports imbalance discussion.

Add to `paper/tables/` when ready; data values are in thesis Cap. 6.6 (verify against rebuilt `meta.csv` before publication).
