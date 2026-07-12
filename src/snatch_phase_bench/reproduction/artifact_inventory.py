"""Inspect artifact files in the read-only snapshot."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


LFS_PREFIX = b"version https://git-lfs.github.com/spec/v1"


@dataclass
class ArtifactStatus:
    path: str
    exists: bool
    size_bytes: int | None
    sha256: str | None
    file_type: str | None
    status: str  # real_binary | git_lfs_pointer | absent | reconstructable
    manifest_sha256: str | None
    manifest_size_bytes: int | None
    notes: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_lfs_pointer(path: Path) -> bool:
    if not path.exists() or path.stat().st_size > 1024:
        return False
    head = path.read_bytes()[:128]
    return head.startswith(b"version https://git-lfs.github.com/spec/v1")


def inspect_artifact(path: Path, manifest_entry: dict[str, Any] | None = None) -> ArtifactStatus:
    rel = str(path)
    manifest_sha = manifest_entry.get("sha256") if manifest_entry else None
    manifest_size = manifest_entry.get("size_bytes") if manifest_entry else None

    if not path.exists():
        return ArtifactStatus(
            path=rel,
            exists=False,
            size_bytes=None,
            sha256=None,
            file_type=None,
            status="absent",
            manifest_sha256=manifest_sha,
            manifest_size_bytes=manifest_size,
            notes="File not found.",
        )

    size = path.stat().st_size
    file_type = "unknown"
    try:
        import subprocess

        file_type = subprocess.check_output(["file", "-b", str(path)], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        file_type = "unavailable"

    if is_lfs_pointer(path):
        return ArtifactStatus(
            path=rel,
            exists=True,
            size_bytes=size,
            sha256=None,
            file_type=file_type,
            status="git_lfs_pointer",
            manifest_sha256=manifest_sha,
            manifest_size_bytes=manifest_size,
            notes="Git LFS pointer stub; real binary not present locally.",
        )

    digest = sha256_file(path)
    matches_manifest = manifest_sha is not None and digest == manifest_sha
    notes = "Real binary present."
    if manifest_sha and not matches_manifest:
        notes = "Real binary present but SHA-256 differs from manifest."
    if manifest_size and size != manifest_size:
        notes += f" Size {size} vs manifest {manifest_size}."

    return ArtifactStatus(
        path=rel,
        exists=True,
        size_bytes=size,
        sha256=digest,
        file_type=file_type,
        status="real_binary",
        manifest_sha256=manifest_sha,
        manifest_size_bytes=manifest_size,
        notes=notes,
    )


def load_manifest_entries(manifest_path: Path) -> dict[str, dict[str, Any]]:
    if not manifest_path.exists():
        return {}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries: dict[str, dict[str, Any]] = {}
    for artifact in manifest.get("artifacts", []):
        entries[str(artifact["path"])] = artifact
    return entries


def inspect_required_artifacts(
    snapshot_root: Path,
    manifest_path: Path,
    artifact_rel_paths: list[str],
    reconstructable: dict[str, str] | None = None,
) -> list[ArtifactStatus]:
    manifest = load_manifest_entries(manifest_path)
    reconstructable = reconstructable or {}
    results: list[ArtifactStatus] = []

    for rel in artifact_rel_paths:
        path = snapshot_root / rel
        entry = manifest.get(rel)
        status = inspect_artifact(path, entry)
        if status.status == "git_lfs_pointer" and rel in reconstructable:
            status.notes += f" Reconstructable: {reconstructable[rel]}"
            status.status = "reconstructable"
        results.append(status)

    return results


def artifacts_to_markdown(results: list[ArtifactStatus]) -> str:
    lines = [
        "# Artifact Inventory",
        "",
        "| File | Status | Size (bytes) | SHA-256 | Manifest match | Notes |",
        "|------|--------|--------------|---------|----------------|-------|",
    ]
    for item in results:
        manifest_match = "—"
        if item.manifest_sha256 and item.sha256:
            manifest_match = "yes" if item.sha256 == item.manifest_sha256 else "no"
        elif item.status == "git_lfs_pointer" and item.manifest_sha256:
            manifest_match = "LFS oid matches manifest"
        lines.append(
            f"| `{item.path}` | {item.status} | {item.size_bytes or '—'} | "
            f"{item.sha256 or '—'} | {manifest_match} | {item.notes} |"
        )
    return "\n".join(lines) + "\n"


def artifacts_to_json(results: list[ArtifactStatus]) -> str:
    return json.dumps([asdict(item) for item in results], indent=2)
