#!/usr/bin/env python3
"""
配置加载器 - 已废弃
请使用: from src.config_loader import ConfigLoader, config_loader
"""

import warnings
from pathlib import Path

warnings.warn(
    "scripts/config_loader.py 已废弃，请使用 from src.config_loader import",
    DeprecationWarning,
    stacklevel=2,
)

# 添加 src 到路径
import sys

src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# 从新位置导入
from config_loader import ConfigLoader, config_loader

__all__ = ["ConfigLoader", "config_loader"]
