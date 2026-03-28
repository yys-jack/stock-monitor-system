#!/usr/bin/env python3
"""
股票服务层 - 已废弃
请使用：from src.stock_service import StockService, stock_service
"""

import warnings
from pathlib import Path

warnings.warn(
    "webapp/services/stock_service.py 已废弃，请使用 from src.stock_service import",
    DeprecationWarning,
    stacklevel=2,
)

# 添加 src 到路径
import sys

src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from stock_service import StockService, stock_service

__all__ = ["StockService", "stock_service"]
