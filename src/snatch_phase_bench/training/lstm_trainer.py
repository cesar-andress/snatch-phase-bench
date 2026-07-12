"""Train LSTM baseline — behavior ported from Paper_TFM-main/scripts/train_lstm_phases.py."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from torch.utils.data import DataLoader, Dataset

from snatch_phase_bench.models.lstm_classifier import LSTMClassifier


class PhaseDataset(Dataset):
    def __init__(self, X: np.ndarray, y: np.ndarray) -> None:
        self.X = torch.from_numpy(X.astype(np.float32, copy=False))
        self.y = torch.from_numpy(y.astype(np.int64, copy=False))

    def __len__(self) -> int:
        return len(self.X)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self.X[index], self.y[index]


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    try:
        torch.use_deterministic_algorithms(True, warn_only=True)
    except TypeError:
        torch.use_deterministic_algorithms(True)


def resolve_device(requested: str) -> torch.device:
    if requested == "cpu":
        return torch.device("cpu")
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is not available.")
        return torch.device("cuda")
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def standardize_by_train(
    X_train: np.ndarray, X_val: np.ndarray, X_test: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mean = X_train.reshape(-1, X_train.shape[-1]).mean(axis=0)
    std = X_train.reshape(-1, X_train.shape[-1]).std(axis=0)
    std[std < 1e-8] = 1.0
    return (
        (X_train - mean) / std,
        (X_val - mean) / std,
        (X_test - mean) / std,
        mean.astype(np.float32),
        std.astype(np.float32),
    )


def class_weights(y: np.ndarray, num_classes: int) -> torch.Tensor:
    counts = np.bincount(y, minlength=num_classes).astype(np.float32)
    counts[counts == 0] = 1.0
    weights = counts.sum() / counts
    return torch.tensor(weights / weights.mean(), dtype=torch.float32)


def run_epoch(
    model: LSTMClassifier,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None = None,
) -> dict[str, Any]:
    training = optimizer is not None
    model.train(training)
    losses: list[float] = []
    predictions: list[int] = []
    targets: list[int] = []

    context = torch.enable_grad() if training else torch.no_grad()
    with context:
        for X_batch, y_batch in loader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)
            if training and optimizer is not None:
                optimizer.zero_grad()
            logits = model(X_batch)
            loss = criterion(logits, y_batch)
            if training and optimizer is not None:
                loss.backward()
                optimizer.step()
            losses.append(float(loss.item()) * len(X_batch))
            predictions.extend(torch.argmax(logits, dim=1).cpu().numpy().tolist())
            targets.extend(y_batch.cpu().numpy().tolist())

    return {
        "loss": sum(losses) / len(loader.dataset),
        "accuracy": float(accuracy_score(targets, predictions)),
        "macro_f1": float(f1_score(targets, predictions, average="macro")),
        "y_true": np.asarray(targets, dtype=np.int64),
        "y_pred": np.asarray(predictions, dtype=np.int64),
    }


def train_lstm_baseline(
    data_dir: Path,
    output_dir: Path,
    split_json: Path,
    *,
    seed: int = 42,
    batch_size: int = 64,
    epochs: int = 40,
    learning_rate: float = 1e-3,
    weight_decay: float = 1e-4,
    hidden_size: int = 128,
    num_layers: int = 1,
    dropout: float = 0.2,
    patience: int = 8,
    device: str = "auto",
) -> dict[str, Any]:
    set_seed(seed)
    device_obj = resolve_device(device)
    data_dir = data_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    X = np.load(data_dir / "X.npy")
    y = np.load(data_dir / "y.npy")
    meta = pd.read_csv(data_dir / "meta.csv")
    split = json.loads(split_json.read_text(encoding="utf-8"))

    if not (len(X) == len(y) == len(meta)):
        raise ValueError("X.npy, y.npy and meta.csv have different lengths.")

    masks = {
        "train": meta["athlete"].astype(str).isin(split["train_athletes"]).to_numpy(),
        "val": meta["athlete"].astype(str).isin(split["val_athletes"]).to_numpy(),
        "test": meta["athlete"].astype(str).isin(split["test_athletes"]).to_numpy(),
    }
    X_train, y_train = X[masks["train"]], y[masks["train"]]
    X_val, y_val = X[masks["val"]], y[masks["val"]]
    X_test, y_test = X[masks["test"]], y[masks["test"]]
    meta_test = meta.loc[masks["test"]].reset_index(drop=True)

    class_ids = sorted(np.unique(y_train).astype(int).tolist())
    class_to_index = {class_id: index for index, class_id in enumerate(class_ids)}
    keep_val = np.isin(y_val, class_ids)
    keep_test = np.isin(y_test, class_ids)
    X_val, y_val = X_val[keep_val], y_val[keep_val]
    X_test, y_test = X_test[keep_test], y_test[keep_test]
    meta_test = meta_test.loc[keep_test].reset_index(drop=True)

    remap = lambda values: np.asarray([class_to_index[int(value)] for value in values], dtype=np.int64)
    y_train_r, y_val_r, y_test_r = remap(y_train), remap(y_val), remap(y_test)
    X_train, X_val, X_test, mean, std = standardize_by_train(X_train, X_val, X_test)

    generator = torch.Generator().manual_seed(seed)
    train_loader = DataLoader(
        PhaseDataset(X_train, y_train_r), batch_size=batch_size, shuffle=True, generator=generator
    )
    val_loader = DataLoader(PhaseDataset(X_val, y_val_r), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(PhaseDataset(X_test, y_test_r), batch_size=batch_size, shuffle=False)

    model = LSTMClassifier(X.shape[-1], hidden_size, num_layers, len(class_ids), dropout).to(device_obj)
    weights = class_weights(y_train_r, len(class_ids)).to(device_obj)
    criterion = nn.CrossEntropyLoss(weight=weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    best_f1 = -1.0
    no_improvement = 0
    history: list[dict[str, Any]] = []
    checkpoint_path = output_dir / "best_model.pt"

    for epoch in range(1, epochs + 1):
        train_result = run_epoch(model, train_loader, criterion, device_obj, optimizer)
        val_result = run_epoch(model, val_loader, criterion, device_obj)
        history.append(
            {
                "epoch": epoch,
                "train_loss": train_result["loss"],
                "train_acc": train_result["accuracy"],
                "train_f1_macro": train_result["macro_f1"],
                "val_loss": val_result["loss"],
                "val_acc": val_result["accuracy"],
                "val_f1_macro": val_result["macro_f1"],
            }
        )
        if val_result["macro_f1"] > best_f1:
            best_f1 = val_result["macro_f1"]
            no_improvement = 0
            torch.save(
                {
                    "model_state_dict": model.state_dict(),
                    "class_ids": class_ids,
                    "input_size": int(X.shape[-1]),
                    "window_size": int(X.shape[1]),
                    "hidden_size": hidden_size,
                    "num_layers": num_layers,
                    "dropout": dropout,
                    "mean": mean,
                    "std": std,
                    "seed": seed,
                    "train_athletes": split["train_athletes"],
                    "val_athletes": split["val_athletes"],
                    "test_athletes": split["test_athletes"],
                },
                checkpoint_path,
            )
        else:
            no_improvement += 1
        if no_improvement >= patience:
            break

    pd.DataFrame(history).to_csv(output_dir / "history.csv", index=False)
    checkpoint = torch.load(checkpoint_path, map_location=device_obj, weights_only=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    test_result = run_epoch(model, test_loader, criterion, device_obj)

    label_map = pd.read_csv(data_dir / "label_map.csv").set_index("phase_id")["phase_name"].to_dict()
    target_names = [str(label_map.get(class_id, f"class_{class_id}")) for class_id in class_ids]
    report = classification_report(
        test_result["y_true"],
        test_result["y_pred"],
        target_names=target_names,
        digits=10,
        zero_division=0,
        output_dict=True,
    )
    matrix = confusion_matrix(test_result["y_true"], test_result["y_pred"])
    (output_dir / "classification_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    pd.DataFrame(matrix, index=target_names, columns=target_names).to_csv(output_dir / "confusion_matrix.csv")

    index_to_class = {index: class_id for index, class_id in enumerate(class_ids)}
    predictions = meta_test.copy()
    predictions["y_true_remap"] = test_result["y_true"]
    predictions["y_pred_remap"] = test_result["y_pred"]
    predictions["y_true_phase_id"] = [index_to_class[int(value)] for value in test_result["y_true"]]
    predictions["y_pred_phase_id"] = [index_to_class[int(value)] for value in test_result["y_pred"]]
    predictions["y_pred_phase_name"] = [label_map.get(value, "unknown") for value in predictions["y_pred_phase_id"]]
    predictions["y_true_phase_name"] = [label_map.get(value, "unknown") for value in predictions["y_true_phase_id"]]
    predictions.to_csv(output_dir / "test_predictions.csv", index=False)

    return {
        "device": str(device_obj),
        "test_samples": int(len(test_result["y_true"])),
        "accuracy": float(test_result["accuracy"]),
        "macro_f1": float(test_result["macro_f1"]),
        "classification_report": report,
        "confusion_matrix_shape": list(matrix.shape),
        "output_dir": str(output_dir),
        "mode": "retraining",
    }
