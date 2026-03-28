#!/usr/bin/env python3
"""
配置加载工具 - 已废弃
请使用：from src.config_loader import ...
"""

import warnings
from pathlib import Path

warnings.warn(
    "webapp/utils/config_loader.py 已废弃，请使用 from src.config_loader import",
    DeprecationWarning,
    stacklevel=2,
)

# 添加 src 到路径
import sys

src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config_loader import (
    ConfigLoader,
    config_loader,
    load_feishu_config,
    load_gold_config,
    load_stocks_config,
    save_stocks_config,
)

__all__ = [
    "ConfigLoader",
    "config_loader",
    "load_stocks_config",
    "load_feishu_config",
    "load_gold_config",
    "save_stocks_config",
]
