"""Tests for processed dataset loader."""

from __future__ import annotations

import pytest

from snatch_phase_bench.config import load_config, output_path
from snatch_phase_bench.data.loaders import load_processed_dataset


def test_load_rebuilt_dataset() -> None:
    config = load_config()
    data_dir = output_path(config, "processed_dir")
    if not (data_dir / "X.npy").exists():
        pytest.skip("Rebuilt dataset not present; run Phase 2 reproduction first.")
    dataset = load_processed_dataset(data_dir)
    assert dataset.num_samples == 21249
    assert dataset.shape == (21249, 31, 99)
