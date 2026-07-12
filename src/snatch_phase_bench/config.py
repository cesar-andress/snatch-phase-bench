"""Load YAML configuration with snapshot path expansion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "configs" / "reproduction.yaml"


def _expand(value: Any, snapshot_root: str) -> Any:
    if isinstance(value, str):
        return value.format(snapshot_root=snapshot_root)
    if isinstance(value, dict):
        return {key: _expand(item, snapshot_root) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand(item, snapshot_root) for item in value]
    return value


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load reproduction config and expand ``{snapshot_root}`` placeholders."""
    config_path = (path or DEFAULT_CONFIG).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid configuration format in {config_path}")

    snapshot_root = str(raw.get("snapshot_root", ""))
    if not snapshot_root:
        raise ValueError("Configuration must define snapshot_root")

    expanded = _expand(raw, snapshot_root=snapshot_root)
    expanded["project_root"] = str(PROJECT_ROOT)
    return expanded


def resolve_path(config: dict[str, Any], key: str) -> Path:
    """Resolve a nested path from config['paths'][key] relative to project root if needed."""
    paths = config.get("paths", {})
    if key not in paths:
        raise KeyError(f"Unknown path key: {key}")
    path = Path(str(paths[key]))
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()


def output_path(config: dict[str, Any], key: str) -> Path:
    """Resolve a path from config['outputs'][key] under project root."""
    outputs = config.get("outputs", {})
    if key not in outputs:
        raise KeyError(f"Unknown output key: {key}")
    path = Path(str(outputs[key]))
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path.resolve()
