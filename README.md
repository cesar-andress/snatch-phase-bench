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

- [`docs/FROZEN_BASELINE.md`](docs/FROZEN_BASELINE.md) — baseline freeze policy
- [`docs/project_architecture.md`](docs/project_architecture.md) — layout and execution flow
- [`docs/research_design.md`](docs/research_design.md) — scientific roadmap
- [`docs/dataset/dataset.md`](docs/dataset/dataset.md) — dataset specification
- [`docs/evaluation_metrics.md`](docs/evaluation_metrics.md) — metric definitions
- [`docs/WORKSPACE_POLICY.md`](docs/WORKSPACE_POLICY.md) — read-only snapshot rules
- [`docs/reproduction/REPRODUCTION_SUMMARY.md`](docs/reproduction/REPRODUCTION_SUMMARY.md) — Phase 2 results (frozen)

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
