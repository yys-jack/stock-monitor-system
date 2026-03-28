#!/usr/bin/env python3
"""
股票预测服务层 - 已废弃
请使用：from src.predictor import StockPredictor
"""

import warnings
from pathlib import Path

warnings.warn(
    "webapp/services/predictor.py 已废弃，请使用 from src.predictor import StockPredictor",
    DeprecationWarning,
    stacklevel=2,
)

# 添加 src 到路径
import sys

src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from predictor import StockPredictor

# 兼容旧代码
PredictorService = StockPredictor

__all__ = ["StockPredictor", "PredictorService"]
