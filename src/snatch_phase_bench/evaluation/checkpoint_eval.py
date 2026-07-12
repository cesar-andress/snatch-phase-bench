"""Evaluate saved LSTM checkpoint — ported from Paper_TFM-main/scripts/evaluate_checkpoint.py."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from torch.utils.data import DataLoader, TensorDataset

from snatch_phase_bench.models.lstm_classifier import LSTMClassifier
from snatch_phase_bench.training.lstm_trainer import resolve_device


def is_lfs_pointer(path: Path) -> bool:
    if not path.exists() or path.stat().st_size > 1024:
        return False
    head = path.read_bytes()[:128]
    return head.startswith(b"version https://git-lfs.github.com/spec/v1")


def evaluate_checkpoint(
    data_dir: Path,
    checkpoint_path: Path,
    split_json: Path,
    *,
    device: str = "auto",
    batch_size: int = 256,
    baseline_report_json: Path | None = None,
) -> dict[str, Any]:
    if is_lfs_pointer(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint is a Git LFS pointer, not a real binary: {checkpoint_path}")

    data_dir = data_dir.resolve()
    checkpoint_path = checkpoint_path.resolve()
    device_obj = resolve_device(device)

    X_path = data_dir / "X.npy"
    if is_lfs_pointer(X_path):
        raise FileNotFoundError(f"X.npy is a Git LFS pointer: {X_path}")

    X = np.load(X_path)
    y = np.load(data_dir / "y.npy")
    meta = pd.read_csv(data_dir / "meta.csv")
    split = json.loads(split_json.read_text(encoding="utf-8"))

    test_mask = meta["athlete"].astype(str).isin(split["test_athletes"]).to_numpy()
    X_test = X[test_mask]
    y_test = y[test_mask]

    checkpoint = torch.load(checkpoint_path, map_location=device_obj, weights_only=False)
    class_ids = [int(value) for value in checkpoint["class_ids"]]
    class_to_index = {class_id: index for index, class_id in enumerate(class_ids)}
    keep = np.isin(y_test, class_ids)
    X_test = X_test[keep]
    y_test = y_test[keep]
    y_test_remapped = np.asarray([class_to_index[int(value)] for value in y_test], dtype=np.int64)

    mean = np.asarray(checkpoint["mean"], dtype=np.float32)
    std = np.asarray(checkpoint["std"], dtype=np.float32)
    X_test = ((X_test - mean) / std).astype(np.float32)

    model = LSTMClassifier(
        input_size=int(checkpoint["input_size"]),
        hidden_size=int(checkpoint["hidden_size"]),
        num_layers=int(checkpoint["num_layers"]),
        num_classes=len(class_ids),
        dropout=float(checkpoint["dropout"]),
    ).to(device_obj)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    loader = DataLoader(
        TensorDataset(torch.from_numpy(X_test), torch.from_numpy(y_test_remapped)),
        batch_size=batch_size,
        shuffle=False,
    )
    predictions: list[int] = []
    targets: list[int] = []
    with torch.no_grad():
        for X_batch, y_batch in loader:
            logits = model(X_batch.to(device_obj))
            predictions.extend(torch.argmax(logits, dim=1).cpu().numpy().tolist())
            targets.extend(y_batch.numpy().tolist())

    y_true = np.asarray(targets, dtype=np.int64)
    y_pred = np.asarray(predictions, dtype=np.int64)
    accuracy = float(accuracy_score(y_true, y_pred))
    macro_f1 = float(f1_score(y_true, y_pred, average="macro"))

    label_map_path = data_dir / "label_map.csv"
    label_map = (
        pd.read_csv(label_map_path).set_index("phase_id")["phase_name"].to_dict()
        if label_map_path.exists()
        else {value: f"class_{value}" for value in class_ids}
    )
    target_names = [str(label_map.get(class_id, f"class_{class_id}")) for class_id in class_ids]
    report = classification_report(
        y_true, y_pred, target_names=target_names, digits=10, zero_division=0, output_dict=True
    )
    matrix = confusion_matrix(y_true, y_pred)

    result: dict[str, Any] = {
        "device": str(device_obj),
        "test_samples": int(len(y_true)),
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
        "confusion_matrix_shape": list(matrix.shape),
        "mode": "checkpoint_evaluation",
        "matches_saved_report": None,
    }

    if baseline_report_json and baseline_report_json.exists():
        saved = json.loads(baseline_report_json.read_text(encoding="utf-8"))
        saved_accuracy = float(saved["accuracy"])
        saved_macro_f1 = float(saved["macro avg"]["f1-score"])
        result["matches_saved_report"] = bool(
            np.isclose(accuracy, saved_accuracy, atol=1e-12)
            and np.isclose(macro_f1, saved_macro_f1, atol=1e-12)
        )
        result["baseline_accuracy"] = saved_accuracy
        result["baseline_macro_f1"] = saved_macro_f1

    return result
