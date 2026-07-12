"""Shared utilities (logging, seeds, paths)."""

from __future__ import annotations

import logging
import random
from pathlib import Path

import numpy as np

try:
    import torch
except ImportError:  # pragma: no cover
    torch = None  # type: ignore


def setup_logging(level: int = logging.INFO) -> None:
    """Configure structured logging for CLI scripts."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def set_seed(seed: int) -> None:
    """Set deterministic seeds where supported."""
    random.seed(seed)
    np.random.seed(seed)
    if torch is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)


def resolve_project_root(start: Path | None = None) -> Path:
    """Return the snatch-phase-bench artifact root (parent of src/)."""
    if start is None:
        start = Path(__file__).resolve()
    for parent in [start, *start.parents]:
        if (parent / "pyproject.toml").exists() and (parent / "src").is_dir():
            return parent
    raise FileNotFoundError("Could not locate project root containing pyproject.toml and src/")
