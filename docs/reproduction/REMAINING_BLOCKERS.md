# Remaining blockers — post Phase 3 benchmark design

**Updated:** 2026-07-13  
**Context:** Baseline reproduction **closed**. Phase 3 benchmark **design complete**; implementation **not** started. Author clarifications integrated in [`AUTHOR_CLARIFICATIONS.md`](AUTHOR_CLARIFICATIONS.md).

---

## Resolved

| Item | Resolution |
|------|------------|
| Checkpoint validation | **VERIFIED** (B1-repro-v1) |
| Benchmark scientific design | [`BENCHMARK_PROTOCOL.md`](../benchmark/BENCHMARK_PROTOCOL.md) |
| Statistical protocol | [`STATISTICAL_PROTOCOL.md`](../benchmark/STATISTICAL_PROTOCOL.md) |
| Governance / versioning | [`BENCHMARK_GOVERNANCE.md`](../benchmark/BENCHMARK_GOVERNANCE.md) |
| Experiment matrix | [`EXPERIMENT_MATRIX.md`](../benchmark/EXPERIMENT_MATRIX.md) |
| Phase definitions | [`AUTHOR_CLARIFICATIONS.md`](AUTHOR_CLARIFICATIONS.md) — seven-phase taxonomy documented |
| Phase ontology code (EXP-ONT) | **`configs/ontology/` + `snatch_phase_bench.ontology`** — mapping layer implemented |
| Annotation protocol | [`AUTHOR_CLARIFICATIONS.md`](AUTHOR_CLARIFICATIONS.md) — single expert, frame-by-frame |
| Frame count discrepancy (37,125 vs 35,825) | **RESOLVED** — 35,825 canonical; duplicates/errors in larger export |
| MediaPipe version | **0.10.30 Full** — documented in [`AUTHOR_CLARIFICATIONS.md`](AUTHOR_CLARIFICATIONS.md) |
| Dataset provenance | **208 clips**, Weightlifting House YouTube, manual trim — documented |

---

## Open blockers (implementation phase)

Ranked by scientific importance:

1. **Benchmark implementation** — B0, B2-core TAS models, boundary evaluator (`boundary.py`), experiment runner
2. **Boundary metric implementation (`boundary.py`)** — **IMPLEMENTED** (frame-canonical; ms requires explicit FPS)
3. **B0 rule-based baseline** — highest reviewer risk; ontology mapping from seven to five phases
4. **B2-core TAS models** — main benchmark table
5. **LOAO / multi-seed uncertainty** — required for inferential claims
6. **Public release policy** — legal / Zenodo clearance; video redistribution rights under evaluation
7. **Inter-annotator agreement** — EXP-IAA (future work; single annotator documented)
8. **Statistical evaluation after benchmark models** — inferential claims pending benchmark runs
9. Camera metadata and robustness studies

See prior detail in [`CHECKPOINT_VALIDATION.md`](CHECKPOINT_VALIDATION.md) companion; implementation order in [`BENCHMARK_PROTOCOL.md`](../benchmark/BENCHMARK_PROTOCOL.md) §11.

---

## Open decisions (require sign-off before coding)

| ID | Decision | Doc reference |
|----|----------|---------------|
| OD-1 | Seven-phase vs mapped five-phase for B0 | BENCHMARK_PROTOCOL §13 |
| OD-2 | B0 knee-angle operational definition | BENCHMARK_PROTOCOL §13 |
| OD-3 | LOAO vs k-fold | STATISTICAL_PROTOCOL §3.3 |
| OD-4 | Seed count (3 vs 5) | STATISTICAL_PROTOCOL §3.1 |
| OD-5 | Early-stop metric for B2 | BENCHMARK_PROTOCOL §13 |
| OD-6 | Reference GPU for runtime | BENCHMARK_PROTOCOL §13 |
| OD-7 | Video public release scope | BENCHMARK_GOVERNANCE §9 |

---

## Recommended first implementation step

**EXP-ONT** (ontology mapping for B0) in parallel with **EXP-MET** (boundary evaluator) — then **EXP-B0**.
