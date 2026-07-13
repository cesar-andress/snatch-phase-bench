"""Frame-wise label storage and ontology-aware label views."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd

from snatch_phase_bench.data.dataset_builder import normalize_relpath, validate_labels
from snatch_phase_bench.ontology.phase_ontology import PhaseOntology


@dataclass(frozen=True)
class FrameLabelSequence:
    """Dense per-frame labels for one video."""

    video_relpath: str
    frames: np.ndarray
    phase_ids: np.ndarray
    phase_names: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.frames) != len(self.phase_ids):
            raise ValueError("frames and phase_ids must have equal length")
        if len(self.phase_names) != len(self.phase_ids):
            raise ValueError("phase_names must align with phase_ids")

    @property
    def num_frames(self) -> int:
        return int(len(self.frames))

    def supervised_mask(self, ontology: PhaseOntology) -> np.ndarray:
        """Boolean mask over frames with supervised phase labels."""
        supervised = set(ontology.supervised_phase_ids)
        return np.array([int(label) in supervised for label in self.phase_ids], dtype=bool)


class FrameLabelStore:
    """
    Read-only access to ``master_frame_labels.csv`` aligned with benchmark ontology.

    Labels are returned as stored in annotations; mapping to alternate ontologies
    happens in the evaluation layer, not here.
    """

    def __init__(
        self,
        labels_csv: Path,
        *,
        ontology: PhaseOntology | None = None,
    ) -> None:
        self.labels_csv = labels_csv.resolve()
        if not self.labels_csv.exists():
            raise FileNotFoundError(f"Labels file not found: {self.labels_csv}")

        raw = pd.read_csv(self.labels_csv)
        self._labels = validate_labels(raw, self.labels_csv)
        self.ontology = ontology

        grouped: dict[str, FrameLabelSequence] = {}
        for video_relpath, group in self._labels.groupby("video_relpath", sort=True):
            ordered = group.sort_values("frame")
            grouped[str(video_relpath)] = FrameLabelSequence(
                video_relpath=str(video_relpath),
                frames=ordered["frame"].to_numpy(dtype=np.int64),
                phase_ids=ordered["phase_id"].to_numpy(dtype=np.int64),
                phase_names=tuple(str(name) for name in ordered["phase_name"].tolist()),
            )
        self._by_video = grouped

    @property
    def video_relpaths(self) -> tuple[str, ...]:
        return tuple(sorted(self._by_video))

    def get(self, video_relpath: str) -> FrameLabelSequence:
        key = normalize_relpath(video_relpath)
        if key not in self._by_video:
            raise KeyError(f"No labels for video: {video_relpath}")
        return self._by_video[key]

    def iter_videos(self) -> Iterator[FrameLabelSequence]:
        for video_relpath in self.video_relpaths:
            yield self._by_video[video_relpath]

    def to_dense_arrays(self, video_relpath: str) -> tuple[np.ndarray, np.ndarray]:
        """Return ``(frames, phase_ids)`` for ``video_relpath``."""
        sequence = self.get(video_relpath)
        return sequence.frames.copy(), sequence.phase_ids.copy()
