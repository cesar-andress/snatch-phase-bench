"""Capture reproducible experiment metadata (environment, git, config)."""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from snatch_phase_bench.benchmark.gpu_runtime import capture_cuda_determinism_settings


def git_commit_hash(repo_root: Path | None = None) -> str | None:
    root = repo_root or Path.cwd()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def git_dirty(repo_root: Path | None = None) -> bool | None:
    root = repo_root or Path.cwd()
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        )
        return bool(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _run_nvidia_smi_query() -> dict[str, str | None]:
    fields = {
        "gpu_name": "name",
        "vram_total_mib": "memory.total",
        "driver_version": "driver_version",
    }
    result: dict[str, str | None] = {key: None for key in fields}
    try:
        query = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        line = query.stdout.strip().splitlines()[0]
        parts = [part.strip() for part in line.split(",")]
        if len(parts) >= 3:
            result["gpu_name"] = parts[0]
            result["vram_total_mib"] = parts[1]
            result["driver_version"] = parts[2]
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError):
        pass
    return result


def _system_ram_kib() -> int | None:
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1])
    except OSError:
        return None
    return None


def capture_environment(*, include_torch: bool = True) -> dict[str, Any]:
    env: dict[str, Any] = {
        "captured_at": datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "system_ram_kib": _system_ram_kib(),
    }
    env.update(_run_nvidia_smi_query())
    if include_torch:
        try:
            import torch

            env["torch_version"] = torch.__version__
            env["cuda_available"] = torch.cuda.is_available()
            env["pytorch_cuda_version"] = torch.version.cuda
            env["cudnn_version"] = torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None
            if torch.cuda.is_available():
                env["cuda_device_name"] = torch.cuda.get_device_name(0)
                env["cuda_device_vram_bytes"] = int(torch.cuda.get_device_properties(0).total_memory)
            env["cuda_determinism"] = capture_cuda_determinism_settings()
        except ImportError:
            env["torch_version"] = None
    try:
        import sklearn

        env["sklearn_version"] = sklearn.__version__
    except ImportError:
        pass
    return env


def validate_reference_hardware(
    *,
    required_device: str = "cuda",
    expected_gpu_substring: str | None = "RTX 4090",
) -> dict[str, Any]:
    """
    Validate that the current machine matches the reference GPU profile.

    Returns a report dict with ``passed`` boolean. Does not raise.
    """
    env = capture_environment()
    checks: list[dict[str, Any]] = []

    cuda_ok = bool(env.get("cuda_available"))
    checks.append(
        {
            "name": "cuda_available",
            "passed": cuda_ok if required_device == "cuda" else True,
            "detail": env.get("cuda_available"),
        }
    )

    gpu_name = env.get("cuda_device_name") or env.get("gpu_name")
    gpu_match = True
    if expected_gpu_substring and gpu_name:
        gpu_match = expected_gpu_substring.lower() in gpu_name.lower()
    elif expected_gpu_substring and required_device == "cuda":
        gpu_match = False
    checks.append(
        {
            "name": "gpu_name",
            "passed": gpu_match if required_device == "cuda" else True,
            "detail": gpu_name,
            "expected_substring": expected_gpu_substring,
        }
    )

    nvidia_smi_ok = env.get("gpu_name") is not None
    checks.append(
        {
            "name": "nvidia_smi",
            "passed": nvidia_smi_ok if required_device == "cuda" else True,
            "detail": env.get("driver_version"),
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "passed": passed,
        "required_device": required_device,
        "expected_gpu_substring": expected_gpu_substring,
        "environment": env,
        "checks": checks,
    }


def load_yaml_snapshot(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def build_protocol_freeze(
    *,
    config_path: Path,
    manifest_path: Path,
    seeds: list[int],
    early_stopping_monitor: str,
    repo_root: Path | None = None,
    reference_hardware: dict[str, Any] | None = None,
    milestone: str = "M3",
) -> dict[str, Any]:
    repo_root = repo_root or Path.cwd()
    hardware_report = validate_reference_hardware(
        required_device=str((reference_hardware or {}).get("device", "cuda")),
        expected_gpu_substring=(reference_hardware or {}).get("gpu"),
    )
    return {
        "frozen_at": datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
        "milestone": milestone,
        "git_commit": git_commit_hash(repo_root),
        "git_dirty": git_dirty(repo_root),
        "seeds": seeds,
        "early_stopping_monitor": early_stopping_monitor,
        "reference_hardware": reference_hardware,
        "hardware_validation": hardware_report,
        "experiment_config_path": str(config_path),
        "experiment_config": load_yaml_snapshot(config_path),
        "benchmark_manifest_path": str(manifest_path),
        "benchmark_manifest": load_yaml_snapshot(manifest_path),
        "environment": capture_environment(),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
