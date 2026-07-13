"""Load ontology and benchmark manifest YAML files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from snatch_phase_bench.ontology.phase_ontology import (
    LabelMapping,
    PhaseDefinition,
    PhaseOntology,
    PhaseTransition,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ONTOLOGY_DIR = PROJECT_ROOT / "configs" / "ontology"
DEFAULT_BENCHMARK_MANIFEST = PROJECT_ROOT / "configs" / "benchmark.yaml"


def _require_dict(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be a mapping")
    return value


def _parse_phases(raw_phases: list[Any]) -> tuple[PhaseDefinition, ...]:
    phases: list[PhaseDefinition] = []
    for entry in raw_phases:
        item = _require_dict(entry, "phase entry")
        phases.append(
            PhaseDefinition(
                phase_id=int(item["id"]),
                name=str(item["name"]),
                supervised=bool(item.get("supervised", True)),
                description=str(item.get("description", "")),
            )
        )
    return tuple(phases)


def _parse_transitions(raw_transitions: list[Any]) -> tuple[PhaseTransition, ...]:
    transitions: list[PhaseTransition] = []
    for entry in raw_transitions:
        item = _require_dict(entry, "transition entry")
        transitions.append(
            PhaseTransition(
                from_phase=str(item["from"]),
                to_phase=str(item["to"]),
                priority=bool(item.get("priority", False)),
            )
        )
    return tuple(transitions)


def load_ontology(path: Path | None = None) -> PhaseOntology:
    """Load a phase ontology YAML file."""
    ontology_path = (path or DEFAULT_ONTOLOGY_DIR / "seven_phase_v1.yaml").resolve()
    if not ontology_path.exists():
        raise FileNotFoundError(f"Ontology file not found: {ontology_path}")

    raw = yaml.safe_load(ontology_path.read_text(encoding="utf-8"))
    document = _require_dict(raw, ontology_path.name)
    meta = _require_dict(document.get("ontology"), f"{ontology_path.name}::ontology")

    return PhaseOntology(
        ontology_id=str(meta["id"]),
        version=str(meta["version"]),
        description=str(meta.get("description", "")),
        phases=_parse_phases(list(document.get("phases", []))),
        transitions=_parse_transitions(list(document.get("transitions", []))),
        references=tuple(str(ref) for ref in meta.get("references", [])),
    )


def load_label_mapping(
    path: Path | None = None,
    *,
    ontology_dir: Path | None = None,
) -> LabelMapping:
    """Load a label-mapping YAML and resolve source/target ontologies."""
    mapping_path = (path or DEFAULT_ONTOLOGY_DIR / "seven_to_five_knee_angle_v1.yaml").resolve()
    if not mapping_path.exists():
        raise FileNotFoundError(f"Mapping file not found: {mapping_path}")

    base_dir = ontology_dir or mapping_path.parent
    raw = yaml.safe_load(mapping_path.read_text(encoding="utf-8"))
    document = _require_dict(raw, mapping_path.name)
    meta = _require_dict(document.get("mapping"), f"{mapping_path.name}::mapping")

    source = load_ontology(base_dir / f"{meta['source_ontology']}.yaml")
    target = load_ontology(base_dir / f"{meta['target_ontology']}.yaml")

    source_to_target: dict[int, int] = {}
    merge_rules: list[str] = []

    for rule in document.get("rules", []):
        item = _require_dict(rule, "mapping rule")
        rule_type = str(item["type"])
        if rule_type == "identity":
            source_name = str(item["source"])
            target_name = str(item["target"])
            source_to_target[source.name_to_id[source_name]] = target.name_to_id[target_name]
        elif rule_type == "merge":
            target_name = str(item["target"])
            target_id = target.name_to_id[target_name]
            for source_name in item["sources"]:
                source_to_target[source.name_to_id[str(source_name)]] = target_id
            rationale = str(item.get("rationale", "")).strip()
            if rationale:
                merge_rules.append(rationale)
        else:
            raise ValueError(f"Unknown mapping rule type: {rule_type}")

    _validate_complete_mapping(source, source_to_target)

    return LabelMapping(
        mapping_id=str(meta["id"]),
        version=str(meta["version"]),
        source=source,
        target=target,
        source_to_target=source_to_target,
        merge_rules=tuple(merge_rules),
        references=tuple(str(ref) for ref in meta.get("references", [])),
    )


def _validate_complete_mapping(source: PhaseOntology, source_to_target: dict[int, int]) -> None:
    missing = set(source.id_to_name) - set(source_to_target)
    if missing:
        names = [source.phase_name(phase_id) for phase_id in sorted(missing)]
        raise ValueError(f"Incomplete mapping for source ontology {source.ontology_id}: {names}")


def load_benchmark_manifest(path: Path | None = None) -> dict[str, Any]:
    """Load the canonical benchmark manifest."""
    manifest_path = (path or DEFAULT_BENCHMARK_MANIFEST).resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"Benchmark manifest not found: {manifest_path}")

    raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid benchmark manifest: {manifest_path}")
    manifest = dict(raw)
    manifest["project_root"] = str(PROJECT_ROOT)
    manifest["_manifest_path"] = str(manifest_path)
    return manifest
