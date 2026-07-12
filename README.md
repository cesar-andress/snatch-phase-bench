# SnatchPhaseBench

Reproducible research artifact for temporal phase segmentation of the Olympic snatch from markerless pose sequences.

**Status:** Phase 1 (audit and scaffolding). No experimental results are claimed in this repository yet.

## Relationship to the original MSc thesis

This project is derived from Adrián Cardona's MSc thesis repository (`Paper_TFM-main`), which is a **strictly read-only archived snapshot**. SnatchPhaseBench will:

1. Reproduce and audit the original LSTM baseline.
2. Redesign evaluation as a proper temporal segmentation benchmark.
3. Compare multiple baseline and stronger temporal models.

**All development, environments, experiments, commits, and pushes happen in this repository only.**

Required reading:

- [`docs/WORKSPACE_POLICY.md`](docs/WORKSPACE_POLICY.md) — read-only rules for `Paper_TFM-main`
- [`docs/REPRODUCTION_PLAN.md`](docs/REPRODUCTION_PLAN.md) — reproduction without modifying the snapshot
- [`docs/audit/PROJECT_AUDIT.md`](docs/audit/PROJECT_AUDIT.md) — phase-1 audit
- [`docs/audit/RESEARCH_ROADMAP.md`](docs/audit/RESEARCH_ROADMAP.md)
- [`docs/audit/QUESTIONS_FOR_STUDENT.md`](docs/audit/QUESTIONS_FOR_STUDENT.md)

## Repository layout

```text
configs/          Experiment YAML configurations
data/             Data staging (raw/interim/processed) — not populated in phase 1
docs/             Additional documentation
outputs/          Generated experiment outputs (gitignored)
scripts/          CLI entry points (to be populated)
src/              Python package (src layout)
tests/            Unit tests for splits, dataset logic, metrics
```

## Quick start

```bash
cd ~/papers/snatch-phase-bench/snatch-phase-bench
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/
```

Do **not** create virtual environments or install packages inside `~/papers/Paper_TFM-main`.

## Data policy

Raw competition videos are **not** included in phase 1. Do not commit large binaries, checkpoints, or personal local paths. See `data/README.md`.

## Citation

See [`CITATION.cff`](CITATION.cff). DOI will be added after Zenodo release.

## License

**TODO — legal review pending.** See [`LICENSE`](LICENSE).
