"""
兼容模块 - 为旧代码提供向后兼容性
导入旧模块将自动重定向到新的 src 模块
"""

import warnings
from pathlib import Path
from typing import Any, Dict, Optional

# 添加 src 到路径
import sys

src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

warnings.warn(
    "scripts 目录下的模块已废弃，请使用 src 模块",
    DeprecationWarning,
    stacklevel=2,
)

# 从新模块导入
from config_loader import ConfigLoader, config_loader


def load_stocks_config() -> Optional[Dict[str, Any]]:
    """加载股票配置（兼容函数）"""
    return config_loader.load_stocks_config()


def load_feishu_config() -> Optional[Dict[str, Any]]:
    """加载飞书配置（兼容函数）"""
    return config_loader.load_feishu_config()


def load_gold_config() -> Optional[Dict[str, Any]]:
    """加载黄金配置（兼容函数）"""
    return config_loader.load_gold_config()


def save_stocks_config(config: Dict[str, Any]) -> bool:
    """保存股票配置（兼容函数）"""
    return config_loader.save_config("stocks_config.json", config)


__all__ = [
    "ConfigLoader",
    "config_loader",
    "load_stocks_config",
    "load_feishu_config",
    "load_gold_config",
    "save_stocks_config",
]
