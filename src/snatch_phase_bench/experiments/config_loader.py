"""Experiment configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from snatch_phase_bench.config import DEFAULT_CONFIG, load_config


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file."""
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"Configuration not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def load_experiment_config(
    experiment_yaml: Path | None = None,
    *,
    merge_reproduction: bool = True,
) -> dict[str, Any]:
    """
    Load experiment YAML and optionally merge snapshot paths from ``reproduction.yaml``.

    Experiment sections: dataset, split, model, optimizer, scheduler, training,
    evaluation, output, expected.
    """
    project_root = DEFAULT_CONFIG.parent.parent
    exp_path = (experiment_yaml or project_root / "configs" / "baseline_lstm.yaml").resolve()
    experiment = load_yaml(exp_path)

    if merge_reproduction and experiment.get("paths", {}).get("use_reproduction_paths", False):
        reproduction = load_config()
        experiment["reproduction"] = reproduction
        experiment["snapshot_root"] = reproduction["snapshot_root"]

    experiment["experiment_config_path"] = str(exp_path)
    return experiment


def get_section(config: dict[str, Any], name: str) -> dict[str, Any]:
    """Return a configuration section or empty dict."""
    section = config.get(name, {})
    if not isinstance(section, dict):
        raise ValueError(f"Configuration section '{name}' must be a mapping.")
    return section
