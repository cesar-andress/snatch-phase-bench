"""Hardware validation tests for MS-TCN benchmark."""

from __future__ import annotations

import warnings

from snatch_phase_bench.benchmark.experiment_metadata import validate_reference_hardware
from snatch_phase_bench.benchmark.gpu_runtime import (
    GpuMemoryTracker,
    capture_cuda_determinism_settings,
    collect_cuda_warnings,
    install_cuda_warning_recorder,
    resolve_cuda_device_index,
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


def test_resolve_cuda_device_index_defaults() -> None:
    assert resolve_cuda_device_index(None) == 0
    assert resolve_cuda_device_index(0) == 0
    assert resolve_cuda_device_index(1) == 1


def test_gpu_memory_tracker_reset_peak_before_cuda_tensors() -> None:
    """Eval calls reset_peak before any CUDA work; must not raise."""
    import torch

    if not torch.cuda.is_available():
        return
    tracker = GpuMemoryTracker(device_index=0)
    tracker.reset_peak()
    tracker.update_peak()
    snapshot = tracker.snapshot()
    assert snapshot["peak_allocated_mib"] >= 0


def test_collect_cuda_warnings_records_cuda_messages() -> None:
    from snatch_phase_bench.benchmark import gpu_runtime as gr

    gr._RECORDED_CUDA_WARNINGS.clear()
    gr._recording_showwarning(
        "CUDA test warning for recorder",
        UserWarning,
        __file__,
        1,
    )
    after = collect_cuda_warnings()
    assert any("CUDA test warning for recorder" in item for item in after)


def test_validate_reference_hardware_report_shape() -> None:
    report = validate_reference_hardware(required_device="cuda", expected_gpu_substring="RTX 4090")
    assert "passed" in report
    assert "checks" in report
    assert "environment" in report
    assert isinstance(report["checks"], list)
