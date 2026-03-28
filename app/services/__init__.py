"""
Services 服务层模块

提供共享的业务逻辑服务
"""

# 从 src 模块导入现有服务，保持向后兼容
from src.config_loader import ConfigLoader, config_loader
from src.gold_service import GoldService, gold_service
from src.stock_service import StockService, stock_service

# 新增服务
from .feishu_service import FeishuService

__all__ = [
    # 配置
    "ConfigLoader",
    "config_loader",
    # 股票服务
    "StockService",
    "stock_service",
    # 黄金服务
    "GoldService",
    "gold_service",
    # 飞书服务
    "FeishuService",
]
