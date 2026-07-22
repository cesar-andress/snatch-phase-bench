"""GPU runtime tracking for benchmark experiments."""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class GpuMemoryTracker:
    """Track peak CUDA memory during training or inference."""

    device_index: int = 0
    peak_allocated_bytes: int = 0
    peak_reserved_bytes: int = 0
    cuda_warnings: list[str] = field(default_factory=list)

    def is_cuda(self) -> bool:
        try:
            import torch

            return torch.cuda.is_available()
        except ImportError:
            return False

    def reset_peak(self) -> None:
        install_cuda_warning_recorder()
        if not self.is_cuda():
            return
        import torch

        torch.cuda.reset_peak_memory_stats(self.device_index)

    def update_peak(self) -> None:
        if not self.is_cuda():
            return
        import torch

        self.peak_allocated_bytes = max(
            self.peak_allocated_bytes,
            int(torch.cuda.max_memory_allocated(self.device_index)),
        )
        self.peak_reserved_bytes = max(
            self.peak_reserved_bytes,
            int(torch.cuda.max_memory_reserved(self.device_index)),
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "peak_allocated_bytes": self.peak_allocated_bytes,
            "peak_allocated_mib": round(self.peak_allocated_bytes / (1024**2), 2),
            "peak_reserved_bytes": self.peak_reserved_bytes,
            "peak_reserved_mib": round(self.peak_reserved_bytes / (1024**2), 2),
            "cuda_warnings": list(self.cuda_warnings),
        }


def capture_cuda_determinism_settings() -> dict[str, Any]:
    try:
        import torch
    except ImportError:
        return {"available": False}

    deterministic_algorithms: bool | str = False
    try:
        deterministic_algorithms = bool(torch.are_deterministic_algorithms_enabled())
    except Exception:
        deterministic_algorithms = "unknown"

    return {
        "cudnn_deterministic": bool(torch.backends.cudnn.deterministic),
        "cudnn_benchmark": bool(torch.backends.cudnn.benchmark),
        "deterministic_algorithms_enabled": deterministic_algorithms,
    }


_RECORDED_CUDA_WARNINGS: list[str] = []
_WARNING_HOOK_INSTALLED = False
_ORIGINAL_SHOWWARNING = warnings.showwarning


def _is_cuda_related(text: str, category_name: str) -> bool:
    haystack = f"{category_name} {text}".lower()
    return any(token in haystack for token in ("cuda", "cudnn", "deterministic"))


def _recording_showwarning(message, category, filename, lineno, file=None, line=None):
    text = str(message)
    category_name = getattr(category, "__name__", str(category))
    if _is_cuda_related(text, category_name):
        entry = f"{category_name}: {text}"
        if entry not in _RECORDED_CUDA_WARNINGS:
            _RECORDED_CUDA_WARNINGS.append(entry)
    return _ORIGINAL_SHOWWARNING(message, category, filename, lineno, file=file, line=line)


def install_cuda_warning_recorder() -> None:
    """Install a process-local ``warnings.showwarning`` hook (idempotent)."""
    global _WARNING_HOOK_INSTALLED
    if _WARNING_HOOK_INSTALLED:
        return
    warnings.showwarning = _recording_showwarning  # type: ignore[assignment]
    _WARNING_HOOK_INSTALLED = True


def collect_cuda_warnings() -> list[str]:
    """Return CUDA-related warnings recorded by the process warning hook.

    Python's ``warnings`` module has no ``getwarnings()`` API; we record via
    ``install_cuda_warning_recorder`` (also called lazily here).
    """
    install_cuda_warning_recorder()
    return list(_RECORDED_CUDA_WARNINGS)
