#!/usr/bin/env python3
"""
飞书推送工具 - 已废弃
请使用：from src.feishu import FeishuNotifier, send_text, send_post
"""

import warnings
from pathlib import Path
from typing import Optional

warnings.warn(
    "webapp/utils/feishu.py 已废弃，请使用 from src.feishu import",
    DeprecationWarning,
    stacklevel=2,
)

# 添加 src 到路径
import sys

src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from feishu import FeishuNotifier, send_post, send_text

# 兼容旧代码
notifier = FeishuNotifier()


def send_feishu_text(content: str, user_id: Optional[str] = None) -> bool:
    """兼容旧函数"""
    return send_text(content, user_id)


__all__ = ["FeishuNotifier", "notifier", "send_text", "send_post", "send_feishu_text"]
