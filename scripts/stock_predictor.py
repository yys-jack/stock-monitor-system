#!/usr/bin/env python3
"""
股票预测功能 - 已废弃
请使用：from src.predictor import StockPredictor
"""

import warnings
from pathlib import Path

warnings.warn(
    "scripts/stock_predictor.py 已废弃，请使用 from src.predictor import StockPredictor",
    DeprecationWarning,
    stacklevel=2,
)

# 添加 src 到路径
import sys

src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from predictor import StockPredictor

__all__ = ["StockPredictor"]


if __name__ == "__main__":
    predictor = StockPredictor("000063")
    predictor.generate_report()
