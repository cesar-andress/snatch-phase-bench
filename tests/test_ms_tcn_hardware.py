"""Hardware validation tests for MS-TCN benchmark."""

from __future__ import annotations

from snatch_phase_bench.benchmark.experiment_metadata import validate_reference_hardware
from snatch_phase_bench.benchmark.gpu_runtime import GpuMemoryTracker, capture_cuda_determinism_settings


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


def test_validate_reference_hardware_report_shape() -> None:
    report = validate_reference_hardware(required_device="cuda", expected_gpu_substring="RTX 4090")
    assert "passed" in report
    assert "checks" in report
    assert "environment" in report
    assert isinstance(report["checks"], list)
