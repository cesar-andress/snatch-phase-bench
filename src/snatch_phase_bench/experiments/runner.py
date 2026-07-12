"""Future experiment runner — baseline remains in frozen reproduction script."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from snatch_phase_bench.experiments.config_loader import load_experiment_config
from snatch_phase_bench.utils.logging import setup_logging

logger = logging.getLogger(__name__)


def run_experiment(experiment_yaml: Path | None = None) -> dict[str, Any]:
    """
    Placeholder for configuration-driven experiments.

    The frozen thesis baseline is executed via ``scripts/run_phase2_reproduction.py``.
    This entry point will dispatch non-baseline models once the checkpoint is validated.
    """
    setup_logging()
    config = load_experiment_config(experiment_yaml)
    name = config.get("experiment", {}).get("name", "unknown")
    model_name = config.get("model", {}).get("name", "unknown")
    logger.info("Experiment config loaded: name=%s model=%s", name, model_name)
    raise NotImplementedError(
        "Generic experiment runner is not enabled while the baseline is frozen. "
        "Use scripts/run_phase2_reproduction.py for the thesis baseline."
    )
