#!/usr/bin/env python3
"""Backward-compatible wrapper around ``run_iaa_pipeline.py``.

Prefer:
  python scripts/run_iaa_pipeline.py
"""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).with_name("run_iaa_pipeline.py")
    runpy.run_path(str(target), run_name="__main__")
