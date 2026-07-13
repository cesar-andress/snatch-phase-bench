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


def capture_environment(*, include_torch: bool = True) -> dict[str, Any]:
    env: dict[str, Any] = {
        "captured_at": datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
    }
    if include_torch:
        try:
            import torch

            env["torch_version"] = torch.__version__
            env["cuda_available"] = torch.cuda.is_available()
            if torch.cuda.is_available():
                env["cuda_device"] = torch.cuda.get_device_name(0)
        except ImportError:
            env["torch_version"] = None
    try:
        import sklearn

        env["sklearn_version"] = sklearn.__version__
    except ImportError:
        pass
    return env


def load_yaml_snapshot(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def build_protocol_freeze(
    *,
    config_path: Path,
    manifest_path: Path,
    seeds: list[int],
    early_stopping_monitor: str,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    repo_root = repo_root or Path.cwd()
    return {
        "frozen_at": datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
        "milestone": "M3",
        "git_commit": git_commit_hash(repo_root),
        "git_dirty": git_dirty(repo_root),
        "seeds": seeds,
        "early_stopping_monitor": early_stopping_monitor,
        "experiment_config_path": str(config_path),
        "experiment_config": load_yaml_snapshot(config_path),
        "benchmark_manifest_path": str(manifest_path),
        "benchmark_manifest": load_yaml_snapshot(manifest_path),
        "environment": capture_environment(),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
