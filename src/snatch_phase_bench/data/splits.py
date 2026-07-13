"""Athlete-level split loading and partitioning helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

SplitName = Literal["train", "val", "test", "unknown"]


@dataclass(frozen=True)
class AthleteSplit:
    """Athlete-disjoint train/validation/test partition."""

    train_athletes: frozenset[str]
    val_athletes: frozenset[str]
    test_athletes: frozenset[str]
    seed: int | None = None
    source_path: Path | None = None

    @classmethod
    def from_json(cls, path: Path) -> AthleteSplit:
        path = path.resolve()
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            train_athletes=frozenset(map(str, payload.get("train_athletes", []))),
            val_athletes=frozenset(map(str, payload.get("val_athletes", []))),
            test_athletes=frozenset(map(str, payload.get("test_athletes", []))),
            seed=int(payload["seed"]) if payload.get("seed") is not None else None,
            source_path=path,
        )

    def partition_for_athlete(self, athlete_id: str) -> SplitName:
        athlete = str(athlete_id)
        if athlete in self.train_athletes:
            return "train"
        if athlete in self.val_athletes:
            return "val"
        if athlete in self.test_athletes:
            return "test"
        return "unknown"

    def athletes_in(self, split: SplitName) -> frozenset[str]:
        if split == "train":
            return self.train_athletes
        if split == "val":
            return self.val_athletes
        if split == "test":
            return self.test_athletes
        raise ValueError(f"Unsupported split name: {split}")

    def filter_video_relpaths(
        self,
        video_relpaths: list[str] | tuple[str, ...],
        *,
        split: SplitName,
    ) -> tuple[str, ...]:
        """Keep videos whose athlete folder belongs to ``split``."""
        allowed = self.athletes_in(split)
        kept: list[str] = []
        for video_relpath in video_relpaths:
            athlete = video_relpath.split("/", 1)[0]
            if athlete in allowed:
                kept.append(video_relpath)
        return tuple(sorted(kept))


def load_athlete_split(path: Path) -> AthleteSplit:
    """Load athlete split JSON from ``path``."""
    return AthleteSplit.from_json(path)
