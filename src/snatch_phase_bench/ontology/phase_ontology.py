"""Core phase ontology and label-mapping types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class PhaseDefinition:
    """Single phase class in an ontology."""

    phase_id: int
    name: str
    supervised: bool = True
    description: str = ""


@dataclass(frozen=True)
class PhaseTransition:
    """Directed transition between consecutive supervised phases."""

    from_phase: str
    to_phase: str
    priority: bool = False


@dataclass(frozen=True)
class PhaseOntology:
    """Immutable phase taxonomy with lookup helpers."""

    ontology_id: str
    version: str
    description: str
    phases: tuple[PhaseDefinition, ...]
    transitions: tuple[PhaseTransition, ...] = ()
    references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        names = [phase.name for phase in self.phases]
        if len(names) != len(set(names)):
            raise ValueError(f"Duplicate phase names in ontology {self.ontology_id}")
        ids = [phase.phase_id for phase in self.phases]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate phase ids in ontology {self.ontology_id}")

    @property
    def id_to_name(self) -> dict[int, str]:
        return {phase.phase_id: phase.name for phase in self.phases}

    @property
    def name_to_id(self) -> dict[str, int]:
        return {phase.name: phase.phase_id for phase in self.phases}

    @property
    def supervised_phase_ids(self) -> tuple[int, ...]:
        return tuple(phase.phase_id for phase in self.phases if phase.supervised)

    @property
    def num_supervised_phases(self) -> int:
        return len(self.supervised_phase_ids)

    def phase_name(self, phase_id: int) -> str:
        if phase_id not in self.id_to_name:
            raise KeyError(f"Unknown phase_id {phase_id} in ontology {self.ontology_id}")
        return self.id_to_name[phase_id]

    def transition_names(self) -> tuple[str, ...]:
        """Return transition keys as ``from->to`` strings in declaration order."""
        return tuple(f"{transition.from_phase}->{transition.to_phase}" for transition in self.transitions)

    def priority_transitions(self) -> tuple[PhaseTransition, ...]:
        return tuple(transition for transition in self.transitions if transition.priority)


@dataclass(frozen=True)
class LabelMapping:
    """Map label ids from a source ontology to a target ontology."""

    mapping_id: str
    version: str
    source: PhaseOntology
    target: PhaseOntology
    source_to_target: dict[int, int]
    merge_rules: tuple[str, ...] = field(default_factory=tuple)
    references: tuple[str, ...] = ()

    def map_label(self, source_id: int) -> int:
        if source_id not in self.source_to_target:
            raise KeyError(
                f"source phase_id {source_id} ({self.source.phase_name(source_id)}) "
                f"has no mapping in {self.mapping_id}"
            )
        return self.source_to_target[source_id]

    def map_labels(self, labels: Iterable[int] | np.ndarray) -> np.ndarray:
        """Vectorized label mapping preserving array shape."""
        array = np.asarray(labels, dtype=np.int64)
        flat = array.ravel()
        mapped = np.array([self.map_label(int(value)) for value in flat], dtype=np.int64)
        return mapped.reshape(array.shape)

    def mapping_table(self) -> list[tuple[str, str]]:
        """Human-readable source→target phase name pairs."""
        rows: list[tuple[str, str]] = []
        for source_id, target_id in sorted(self.source_to_target.items()):
            rows.append(
                (
                    self.source.phase_name(source_id),
                    self.target.phase_name(target_id),
                )
            )
        return rows
