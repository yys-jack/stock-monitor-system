#!/usr/bin/env python3
"""
日志配置模块 - 已废弃
请使用：from src.logging_config import setup_logger, LOG_LEVELS
"""

import warnings
from pathlib import Path

warnings.warn(
    "scripts/logging_config.py 已废弃，请使用 from src.logging_config import",
    DeprecationWarning,
    stacklevel=2,
)

# 添加 src 到路径
import sys

src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from logging_config import LOG_LEVELS, setup_logger

__all__ = ["setup_logger", "LOG_LEVELS"]
