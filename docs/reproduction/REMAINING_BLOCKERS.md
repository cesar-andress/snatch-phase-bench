# Remaining blockers — post B0 freeze / MS-TCN infrastructure

**Updated:** 2026-07-14  
**Context:** B0 **frozen as exploratory reference** (accepted audit outcome). MS-TCN **infrastructure ready**; architecture **not implemented**.

---

## Resolved

| Item | Resolution |
|------|------------|
| B0 evidence audit | [`B0_EVIDENCE_MATRIX.md`](../benchmark/B0_EVIDENCE_MATRIX.md) |
| B0 scope decision | **Frozen exploratory reference** — [`B0_EXPLORATORY_REFERENCE.md`](../benchmark/B0_EXPLORATORY_REFERENCE.md) |
| Boundary metric implementation | **IMPLEMENTED** (`evaluation/metrics/boundary.py`) |
| Phase ontology (EXP-ONT) | **`configs/ontology/` + `snatch_phase_bench.ontology`** |
| MS-TCN model + trainer (M2) | **`models/ms_tcn/` + `training/ms_tcn_trainer.py`** |
| Frame-sequence dataset adapter | `snatch_phase_bench.data.frame_sequence` |
| TAS evaluation hooks | `snatch_phase_bench.evaluation.tas_hooks` |
| Benchmark model registry | `snatch_phase_bench.benchmark.registry` |

---

## Open blockers (implementation phase)

Ranked by scientific importance:

1. **MS-TCN multi-seed benchmark runs** — implementation complete; test-set evaluation pending
2. **MS-TCN++ and ASFormer** — extended B2 family
3. **Experiment runner** — wire config → train → evaluate → JSON output
4. **LOAO / multi-seed uncertainty** — required for inferential claims
5. **Public release policy** — legal / Zenodo clearance
6. **Inter-annotator agreement** — EXP-IAA (future work)
7. **Native FPS verification** — required before reporting boundary ms
8. Camera metadata and robustness studies

---

## Closed decisions

| ID | Decision | Outcome |
|----|----------|---------|
| OD-1 | B0 competitive scope | **Closed** — exploratory reference only |
| OD-2 | B0 knee-angle operational definition | **Closed** — insufficient evidence; no implementation |

---

## Open decisions (require sign-off before B2 training runs)

| ID | Decision | Doc reference |
|----|----------|---------------|
| OD-5 | Early-stop metric for B2 | BENCHMARK_PROTOCOL §13 |
| OD-6 | Reference GPU for runtime | BENCHMARK_PROTOCOL §13 |
| OD-3 | LOAO vs k-fold | STATISTICAL_PROTOCOL §3.3 |
| OD-4 | Seed count (3 vs 5) | STATISTICAL_PROTOCOL §3.1 |
| OD-7 | Video public release scope | BENCHMARK_GOVERNANCE §9 |

---

## Recommended next implementation step

1. Implement **MS-TCN** (`models/ms_tcn.py`, trainer, registry entry).
2. Enable **experiment runner** for B2 configs (`configs/benchmark/ms_tcn.yaml`).
3. Run **test-split evaluation** → canonical JSON via `evaluate_frame_predictions()`.

Do **not** reopen B0 unless new evidence resolves audit gaps with documented provenance.
