"""Unit tests for athlete-paired bootstrap helper."""

from __future__ import annotations

import numpy as np

from scripts.run_athlete_paired_bootstrap import paired_bootstrap, _ci_includes_zero


def test_paired_bootstrap_known_difference_excludes_zero() -> None:
    rng = np.random.default_rng(0)
    a = rng.normal(0.70, 0.02, size=11)
    b = a + 0.05
    _, _, diff, samples = paired_bootstrap(a, b, n_boot=2000, seed=42)
    assert diff.mean == np.mean(samples)
    assert abs(diff.mean - 0.05) < 0.01
    assert not _ci_includes_zero(diff)


def test_paired_bootstrap_identical_includes_zero() -> None:
    a = np.linspace(0.5, 0.9, 11)
    b = a.copy()
    _, _, diff, _ = paired_bootstrap(a, b, n_boot=2000, seed=42)
    assert abs(diff.mean) < 1e-12
    assert _ci_includes_zero(diff)
