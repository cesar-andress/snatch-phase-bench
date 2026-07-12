"""
Build sliding-window pose dataset from frame labels and keypoint CSVs.

Ported from Paper_TFM-main/scripts/build_phase_dataset.py with configurable paths only.
Scientific behavior preserved.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def normalize_relpath(value: str) -> str:
    return str(value).replace("\\", "/").strip()


def get_keypoint_csv_path(keypoints_dir: Path, video_relpath: str) -> Path:
    return keypoints_dir / Path(video_relpath).with_suffix(".csv")


def get_athlete_from_relpath(video_relpath: str) -> str:
    parts = Path(video_relpath).parts
    return parts[0] if len(parts) >= 2 else "unknown"


def get_feature_columns(df: pd.DataFrame, use_z: bool, use_visibility: bool) -> list[str]:
    columns: list[str] = []
    for i in range(33):
        columns.extend([f"x{i}", f"y{i}"])
        if use_z:
            columns.append(f"z{i}")
        if use_visibility:
            columns.append(f"v{i}")

    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing keypoint columns: {missing[:10]}")
    return columns


def validate_labels(labels_df: pd.DataFrame, labels_csv: Path) -> pd.DataFrame:
    required = {"video_relpath", "frame", "phase_id", "phase_name"}
    missing = required - set(labels_df.columns)
    if missing:
        raise ValueError(f"Missing columns in {labels_csv}: {sorted(missing)}")

    labels_df = labels_df.copy()
    labels_df["video_relpath"] = labels_df["video_relpath"].astype(str).map(normalize_relpath)
    labels_df["frame"] = pd.to_numeric(labels_df["frame"], errors="coerce")
    labels_df["phase_id"] = pd.to_numeric(labels_df["phase_id"], errors="coerce")
    labels_df = labels_df.dropna(subset=["video_relpath", "frame", "phase_id"]).copy()
    labels_df["frame"] = labels_df["frame"].astype(int)
    labels_df["phase_id"] = labels_df["phase_id"].astype(int)

    duplicated = labels_df.duplicated(["video_relpath", "frame"], keep=False)
    if duplicated.any():
        duplicate_rows = labels_df.loc[duplicated, ["video_relpath", "frame", "phase_id", "phase_name"]]
        conflicting = (
            duplicate_rows.groupby(["video_relpath", "frame"])["phase_id"].nunique().gt(1).sum()
        )
        raise ValueError(
            f"{labels_csv} contains {int(duplicated.sum())} duplicated rows; "
            f"{int(conflicting)} pairs have conflicting labels."
        )

    return labels_df.sort_values(["video_relpath", "frame"]).reset_index(drop=True)


def load_and_prepare_pose_csv(pose_csv: Path, feature_cols: list[str]) -> pd.DataFrame:
    pose_df = pd.read_csv(pose_csv)
    if "frame" not in pose_df.columns:
        raise ValueError(f"Missing 'frame' column in {pose_csv}")

    pose_df["frame"] = pd.to_numeric(pose_df["frame"], errors="coerce")
    pose_df = pose_df.dropna(subset=["frame"]).copy()
    pose_df["frame"] = pose_df["frame"].astype(int)
    pose_df[feature_cols] = pose_df[feature_cols].apply(pd.to_numeric, errors="coerce")
    pose_df[feature_cols] = pose_df[feature_cols].interpolate(limit_direction="both")
    pose_df[feature_cols] = pose_df[feature_cols].ffill().bfill()
    return pose_df.sort_values("frame").drop_duplicates(subset=["frame"]).reset_index(drop=True)


def build_windows_for_video(
    merged_df: pd.DataFrame,
    feature_cols: list[str],
    window_size: int,
    stride: int,
    drop_unlabeled: bool,
    drop_windows_with_nan: bool,
) -> tuple[list[np.ndarray], list[int], list[dict[str, Any]]]:
    if window_size % 2 == 0:
        raise ValueError("window_size must be odd.")
    if stride < 1:
        raise ValueError("stride must be at least 1.")

    half = window_size // 2
    merged_df = merged_df.sort_values("frame").reset_index(drop=True)
    features = merged_df[feature_cols].to_numpy(dtype=np.float32)
    labels = merged_df["phase_id"].to_numpy(dtype=np.int64)
    frames = merged_df["frame"].to_numpy(dtype=np.int64)
    video_relpath = str(merged_df["video_relpath"].iloc[0])
    athlete = get_athlete_from_relpath(video_relpath)

    X_list: list[np.ndarray] = []
    y_list: list[int] = []
    meta_list: list[dict[str, Any]] = []

    for center_idx in range(half, len(merged_df) - half, stride):
        start_idx = center_idx - half
        end_idx = center_idx + half + 1
        window_x = features[start_idx:end_idx]
        center_label = int(labels[center_idx])

        if drop_unlabeled and center_label == 0:
            continue
        if drop_windows_with_nan and np.isnan(window_x).any():
            continue

        X_list.append(window_x)
        y_list.append(center_label)
        meta_list.append(
            {
                "video_relpath": video_relpath,
                "athlete": athlete,
                "center_frame": int(frames[center_idx]),
                "start_frame": int(frames[start_idx]),
                "end_frame": int(frames[end_idx - 1]),
                "phase_id": center_label,
                "phase_name": str(merged_df["phase_name"].iloc[center_idx]),
            }
        )

    return X_list, y_list, meta_list


def build_phase_dataset(
    labels_csv: Path,
    keypoints_dir: Path,
    output_dir: Path,
    *,
    window_size: int = 31,
    stride: int = 1,
    use_z: bool = True,
    use_visibility: bool = False,
    drop_unlabeled: bool = True,
    drop_windows_with_nan: bool = False,
) -> dict[str, Any]:
    """Build and save X.npy, y.npy, meta.csv, label_map.csv."""
    labels_csv = labels_csv.resolve()
    keypoints_dir = keypoints_dir.resolve()
    output_dir = output_dir.resolve()

    if not labels_csv.exists():
        raise FileNotFoundError(f"Labels file not found: {labels_csv}")
    if not keypoints_dir.exists():
        raise FileNotFoundError(f"Keypoints directory not found: {keypoints_dir}")

    labels_df = validate_labels(pd.read_csv(labels_csv), labels_csv)
    output_dir.mkdir(parents=True, exist_ok=True)

    X_all: list[np.ndarray] = []
    y_all: list[int] = []
    meta_all: list[dict[str, Any]] = []
    videos = sorted(labels_df["video_relpath"].unique())
    missing_keypoints: list[str] = []

    for video_relpath in videos:
        pose_csv = get_keypoint_csv_path(keypoints_dir, video_relpath)
        if not pose_csv.exists():
            missing_keypoints.append(str(video_relpath))
            continue

        raw_pose = pd.read_csv(pose_csv, nrows=1)
        feature_cols = get_feature_columns(raw_pose, use_z=use_z, use_visibility=use_visibility)
        pose_df = load_and_prepare_pose_csv(pose_csv, feature_cols)
        pose_df["video_relpath"] = video_relpath

        video_labels = labels_df[labels_df["video_relpath"] == video_relpath]
        merged_df = pd.merge(
            video_labels[["video_relpath", "frame", "phase_id", "phase_name"]],
            pose_df[["video_relpath", "frame"] + feature_cols],
            on=["video_relpath", "frame"],
            how="inner",
            validate="one_to_one",
        )
        if merged_df.empty:
            raise RuntimeError(f"No aligned labels/keypoints for {video_relpath}")

        X_video, y_video, meta_video = build_windows_for_video(
            merged_df=merged_df,
            feature_cols=feature_cols,
            window_size=window_size,
            stride=stride,
            drop_unlabeled=drop_unlabeled,
            drop_windows_with_nan=drop_windows_with_nan,
        )
        X_all.extend(X_video)
        y_all.extend(y_video)
        meta_all.extend(meta_video)

    if missing_keypoints:
        raise FileNotFoundError(
            "Missing keypoints for videos:\n" + "\n".join(missing_keypoints[:20])
        )
    if not X_all:
        raise RuntimeError("No samples were generated.")

    X = np.stack(X_all).astype(np.float32)
    y = np.asarray(y_all, dtype=np.int64)
    meta_df = pd.DataFrame(meta_all)
    label_map_df = (
        labels_df[["phase_id", "phase_name"]]
        .drop_duplicates()
        .sort_values("phase_id")
        .reset_index(drop=True)
    )

    np.save(output_dir / "X.npy", X)
    np.save(output_dir / "y.npy", y)
    meta_df.to_csv(output_dir / "meta.csv", index=False)
    label_map_df.to_csv(output_dir / "label_map.csv", index=False)

    return {
        "videos": len(videos),
        "samples": int(len(X)),
        "X_shape": list(X.shape),
        "y_shape": list(y.shape),
        "output_dir": str(output_dir),
    }
