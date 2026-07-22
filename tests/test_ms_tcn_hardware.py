"""Hardware validation tests for MS-TCN benchmark."""

from __future__ import annotations

import warnings

from snatch_phase_bench.benchmark.experiment_metadata import validate_reference_hardware
from snatch_phase_bench.benchmark.gpu_runtime import (
    GpuMemoryTracker,
    capture_cuda_determinism_settings,
    collect_cuda_warnings,
    install_cuda_warning_recorder,
)


def test_gpu_memory_tracker_cpu_snapshot() -> None:
    tracker = GpuMemoryTracker()
    snapshot = tracker.snapshot()
    assert snapshot["peak_allocated_bytes"] == 0
    assert snapshot["peak_reserved_bytes"] == 0
    assert snapshot["cuda_warnings"] == []


def test_cuda_determinism_settings_structure() -> None:
    settings = capture_cuda_determinism_settings()
    assert "cudnn_deterministic" in settings
    assert "cudnn_benchmark" in settings


def test_collect_cuda_warnings_records_cuda_messages() -> None:
    install_cuda_warning_recorder()
    before = set(collect_cuda_warnings())
    warnings.warn("CUDA test warning for recorder", UserWarning)
    after = collect_cuda_warnings()
    assert any("CUDA test warning for recorder" in item for item in after)
    assert set(after) >= before


def test_validate_reference_hardware_report_shape() -> None:
    report = validate_reference_hardware(required_device="cuda", expected_gpu_substring="RTX 4090")
    assert "passed" in report
    assert "checks" in report
    assert "environment" in report
    assert isinstance(report["checks"], list)
