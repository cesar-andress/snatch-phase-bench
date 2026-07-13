"""Deterministic MS-TCN training, checkpointing, and inference."""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader, Dataset

from snatch_phase_bench.data.frame_sequence import FrameSequenceRecord
from snatch_phase_bench.models.base import TemporalSegmentationModel
from snatch_phase_bench.models.ms_tcn.loss import compute_mstcn_loss
from snatch_phase_bench.models.ms_tcn.model import MSTCNModel
from snatch_phase_bench.training.interfaces import (
    TemporalSegmentationTrainer,
    TrainerConfig,
    TrainingRunContext,
)
from snatch_phase_bench.training.lstm_trainer import class_weights, resolve_device, set_seed, standardize_by_train

logger = logging.getLogger(__name__)

CHECKPOINT_VERSION = "mstcn-v1"


class FrameSequenceDataset(Dataset):
    """One video per item for variable-length MS-TCN training."""

    def __init__(
        self,
        records: list[FrameSequenceRecord],
        mean: np.ndarray,
        std: np.ndarray,
    ) -> None:
        self.records = records
        self.mean = mean.astype(np.float32)
        self.std = std.astype(np.float32)

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor, str]:
        record = self.records[index]
        features = ((record.features - self.mean) / self.std).astype(np.float32)
        labels = record.phase_ids.astype(np.int64)
        return torch.from_numpy(features), torch.from_numpy(labels), record.video_relpath


def _collate_single(batch: list[tuple[torch.Tensor, torch.Tensor, str]]) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, list[str]]:
    if len(batch) != 1:
        raise ValueError("MS-TCN collate expects batch_size=1 for variable-length videos.")
    features, labels, video_id = batch[0]
    features = features.unsqueeze(0)
    labels = labels.unsqueeze(0)
    mask = torch.ones(1, labels.shape[1], dtype=features.dtype)
    return features, labels, mask, [video_id]


def _compute_standardization(
    records: list[FrameSequenceRecord],
) -> tuple[np.ndarray, np.ndarray]:
    if not records:
        raise ValueError("Cannot compute standardization without training records.")
    stacked = np.concatenate([record.features for record in records], axis=0)
    mean = stacked.mean(axis=0).astype(np.float32)
    std = stacked.std(axis=0).astype(np.float32)
    std[std < 1e-8] = 1.0
    return mean, std


def _macro_f1_supervised(y_true: np.ndarray, y_pred: np.ndarray, ignore_label_id: int) -> float:
    mask = y_true != ignore_label_id
    if not mask.any():
        return 0.0
    return float(
        f1_score(
            y_true[mask],
            y_pred[mask],
            average="macro",
            zero_division=0,
        )
    )


class MSTCNTrainer(TemporalSegmentationTrainer):
    """Paper-faithful MS-TCN trainer with benchmark hooks."""

    def __init__(
        self,
        *,
        num_classes: int = 8,
        tmse_weight: float = 0.15,
        tmse_truncate_tau: float = 4.0,
        use_amp: bool = False,
        log_dir: Path | None = None,
    ) -> None:
        self.num_classes = num_classes
        self.tmse_weight = tmse_weight
        self.tmse_truncate_tau = tmse_truncate_tau
        self.use_amp = use_amp
        self.log_dir = log_dir
        self._writer: Any | None = None

    def _get_writer(self, log_dir: Path | None) -> Any | None:
        if log_dir is None:
            return None
        if self._writer is not None:
            return self._writer
        try:
            from torch.utils.tensorboard import SummaryWriter
        except ImportError:
            logger.warning("TensorBoard not available; training metrics will not be logged to TB.")
            return None
        log_dir.mkdir(parents=True, exist_ok=True)
        self._writer = SummaryWriter(log_dir=str(log_dir))
        return self._writer

    def fit(
        self,
        train_records: list[FrameSequenceRecord],
        val_records: list[FrameSequenceRecord],
        *,
        model: TemporalSegmentationModel,
        config: TrainerConfig,
        context: TrainingRunContext,
    ) -> TemporalSegmentationModel:
        if not isinstance(model, MSTCNModel):
            raise TypeError("MSTCNTrainer requires MSTCNModel.")

        set_seed(context.seed)
        device = resolve_device(config.device)
        output_dir = context.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        mean, std = _compute_standardization(train_records)
        np.save(output_dir / "feature_mean.npy", mean)
        np.save(output_dir / "feature_std.npy", std)

        train_loader = DataLoader(
            FrameSequenceDataset(train_records, mean, std),
            batch_size=config.batch_size,
            shuffle=True,
            collate_fn=_collate_single,
        )
        val_loader = DataLoader(
            FrameSequenceDataset(val_records, mean, std),
            batch_size=1,
            shuffle=False,
            collate_fn=_collate_single,
        )

        model = model.to(device)
        train_labels = np.concatenate([record.phase_ids for record in train_records], axis=0)
        weights = None
        if config.class_weighting:
            weights = class_weights(train_labels, self.num_classes).to(device)
        ce_loss = nn.CrossEntropyLoss(weight=weights, ignore_index=config.ignore_label_id)
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=config.learning_rate,
            weight_decay=getattr(config, "weight_decay", 0.0),
        )

        scaler = torch.amp.GradScaler("cuda", enabled=self.use_amp and device.type == "cuda")
        writer = self._get_writer(self.log_dir or output_dir / "tensorboard")

        best_metric = float("-inf")
        best_state: dict[str, Any] | None = None
        patience_counter = 0
        history: list[dict[str, Any]] = []
        start_epoch = 0

        resume_path = output_dir / "checkpoint_last.pt"
        if resume_path.exists():
            payload = torch.load(resume_path, map_location=device, weights_only=False)
            model.load_state_dict(payload["model_state_dict"])
            optimizer.load_state_dict(payload["optimizer_state_dict"])
            start_epoch = int(payload.get("epoch", 0))
            best_metric = float(payload.get("best_metric", best_metric))
            patience_counter = int(payload.get("patience_counter", 0))
            if "scaler_state_dict" in payload and scaler.is_enabled():
                scaler.load_state_dict(payload["scaler_state_dict"])
            logger.info("Resumed MS-TCN training from epoch %s", start_epoch)

        for epoch in range(start_epoch + 1, config.epochs + 1):
            train_metrics = self._run_epoch(
                model,
                train_loader,
                device,
                ce_loss,
                optimizer=optimizer,
                scaler=scaler,
                ignore_label_id=config.ignore_label_id,
            )
            val_metrics = self._run_epoch(
                model,
                val_loader,
                device,
                ce_loss,
                ignore_label_id=config.ignore_label_id,
            )
            monitor_value = val_metrics.get(config.early_stopping_monitor, val_metrics["macro_f1"])
            history.append(
                {
                    "epoch": epoch,
                    "train": train_metrics,
                    "val": val_metrics,
                    "monitor": monitor_value,
                }
            )

            if writer is not None:
                writer.add_scalar("loss/train", train_metrics["loss_total"], epoch)
                writer.add_scalar("loss/val", val_metrics["loss_total"], epoch)
                writer.add_scalar("macro_f1/train", train_metrics["macro_f1"], epoch)
                writer.add_scalar("macro_f1/val", val_metrics["macro_f1"], epoch)

            logger.info(
                "Epoch %s/%s train_loss=%.4f val_loss=%.4f val_macro_f1=%.4f",
                epoch,
                config.epochs,
                train_metrics["loss_total"],
                val_metrics["loss_total"],
                val_metrics["macro_f1"],
            )

            improved = monitor_value > best_metric
            if improved:
                best_metric = monitor_value
                best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
                patience_counter = 0
                self.save_checkpoint(
                    model,
                    output_dir / "best_model.pt",
                    context=context,
                    metrics={"epoch": epoch, "best_metric": best_metric, "val": val_metrics},
                    extra={"mean": mean, "std": std, "model_state_dict": model.state_dict()},
                )
            else:
                patience_counter += 1

            torch.save(
                {
                    "checkpoint_version": CHECKPOINT_VERSION,
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "scaler_state_dict": scaler.state_dict() if scaler.is_enabled() else None,
                    "best_metric": best_metric,
                    "patience_counter": patience_counter,
                    "context": asdict(context),
                },
                resume_path,
            )

            if patience_counter >= config.early_stopping_patience:
                logger.info("Early stopping at epoch %s (monitor=%s)", epoch, config.early_stopping_monitor)
                break

        (output_dir / "history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
        if best_state is not None:
            model.load_state_dict(best_state)
        if writer is not None:
            writer.close()
        return model

    def _run_epoch(
        self,
        model: MSTCNModel,
        loader: DataLoader,
        device: torch.device,
        ce_loss: nn.Module,
        *,
        optimizer: torch.optim.Optimizer | None = None,
        scaler: torch.amp.GradScaler | None = None,
        ignore_label_id: int,
    ) -> dict[str, float]:
        training = optimizer is not None
        model.train(training)

        loss_totals: list[float] = []
        y_true_all: list[int] = []
        y_pred_all: list[int] = []

        for features, labels, mask, _video_ids in loader:
            features = features.to(device)
            labels = labels.to(device)
            mask_conv = mask.unsqueeze(1).to(device)

            if training and optimizer is not None:
                optimizer.zero_grad(set_to_none=True)

            with torch.set_grad_enabled(training):
                if training and scaler is not None and scaler.is_enabled():
                    with torch.autocast(device_type=device.type, enabled=True):
                        stage_logits = model.forward_stages(features, mask=mask_conv)
                        loss, loss_metrics = compute_mstcn_loss(
                            stage_logits,
                            labels,
                            mask=mask_conv,
                            ce_loss=ce_loss,
                            tmse_weight=self.tmse_weight,
                            tmse_truncate_tau=self.tmse_truncate_tau,
                        )
                    scaler.scale(loss).backward()
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    stage_logits = model.forward_stages(features, mask=mask_conv)
                    loss, loss_metrics = compute_mstcn_loss(
                        stage_logits,
                        labels,
                        mask=mask_conv,
                        ce_loss=ce_loss,
                        tmse_weight=self.tmse_weight,
                        tmse_truncate_tau=self.tmse_truncate_tau,
                    )
                    if training and optimizer is not None:
                        loss.backward()
                        optimizer.step()

            loss_totals.append(float(loss_metrics["loss_total"]))
            with torch.no_grad():
                preds = torch.argmax(stage_logits[-1], dim=1).squeeze(0).cpu().numpy()
                targets = labels.squeeze(0).cpu().numpy()
            y_true_all.extend(targets.tolist())
            y_pred_all.extend(preds.tolist())

        y_true = np.asarray(y_true_all, dtype=np.int64)
        y_pred = np.asarray(y_pred_all, dtype=np.int64)
        return {
            "loss_total": float(np.mean(loss_totals)) if loss_totals else 0.0,
            "macro_f1": _macro_f1_supervised(y_true, y_pred, ignore_label_id),
        }

    def predict_records(
        self,
        records: list[FrameSequenceRecord],
        *,
        model: TemporalSegmentationModel,
        device: torch.device,
        mean: np.ndarray | None = None,
        std: np.ndarray | None = None,
    ) -> dict[str, np.ndarray]:
        if not isinstance(model, MSTCNModel):
            raise TypeError("MSTCNTrainer requires MSTCNModel.")
        model = model.to(device)
        model.eval()

        if mean is None or std is None:
            mean = np.zeros(records[0].feature_dim, dtype=np.float32)
            std = np.ones(records[0].feature_dim, dtype=np.float32)

        predictions: dict[str, np.ndarray] = {}
        with torch.no_grad():
            for record in records:
                features = ((record.features - mean) / std).astype(np.float32)
                tensor = torch.from_numpy(features).unsqueeze(0).to(device)
                pred = model.predict_classes(tensor).squeeze(0).cpu().numpy().astype(np.int64)
                predictions[record.video_relpath] = pred
        return predictions

    def predict_video(
        self,
        features: np.ndarray,
        *,
        model: MSTCNModel,
        device: torch.device,
        mean: np.ndarray,
        std: np.ndarray,
    ) -> np.ndarray:
        """Predict a single video from ``(T, D)`` features."""
        standardized = ((features - mean) / std).astype(np.float32)
        tensor = torch.from_numpy(standardized).unsqueeze(0).to(device)
        model.eval()
        with torch.no_grad():
            return model.predict_classes(tensor).squeeze(0).cpu().numpy().astype(np.int64)

    def save_checkpoint(
        self,
        model: TemporalSegmentationModel,
        path: Path,
        *,
        context: TrainingRunContext,
        metrics: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {
            "checkpoint_version": CHECKPOINT_VERSION,
            "model_name": model.name,
            "model_state_dict": model.state_dict(),
            "context": asdict(context),
            "metrics": metrics or {},
        }
        if extra:
            payload.update(extra)
        torch.save(payload, path)

    def load_checkpoint(
        self,
        path: Path,
        *,
        model: TemporalSegmentationModel,
    ) -> TemporalSegmentationModel:
        payload = torch.load(path, map_location="cpu", weights_only=False)
        model.load_state_dict(payload["model_state_dict"])
        return model

    @staticmethod
    def load_standardization(checkpoint_dir: Path) -> tuple[np.ndarray, np.ndarray]:
        mean = np.load(checkpoint_dir / "feature_mean.npy")
        std = np.load(checkpoint_dir / "feature_std.npy")
        return mean, std
