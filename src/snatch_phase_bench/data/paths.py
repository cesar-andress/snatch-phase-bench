"""Path helpers for read-only snapshot and canonical outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from snatch_phase_bench.config import load_config, output_path, resolve_path


def get_snapshot_root(config: dict[str, Any] | None = None) -> Path:
    """Return read-only student snapshot root."""
    cfg = config or load_config()
    return Path(str(cfg["snapshot_root"])).resolve()


def get_processed_dir(config: dict[str, Any] | None = None) -> Path:
    """Return canonical processed tensor directory."""
    cfg = config or load_config()
    return output_path(cfg, "processed_dir")


def get_split_json(config: dict[str, Any] | None = None) -> Path:
    """Return athlete split JSON path (read-only snapshot)."""
    cfg = config or load_config()
    return resolve_path(cfg, "athlete_split_json")
