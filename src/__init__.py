"""
股票监控系统核心模块

提供统一的配置加载、日志记录、股票/黄金服务、预测功能和飞书推送

Example usage:
    from src import (
        ConfigLoader, config_loader,
        StockService, stock_service,
        GoldService, gold_service,
        StockPredictor,
        FeishuNotifier, send_text,
        setup_logger,
    )
"""

__version__ = "5.6.0"
__author__ = "yys-jack"

# 导入所有公共模块
from .config_loader import ConfigLoader, config_loader
from .feishu import FeishuNotifier, send_post, send_text
from .gold_service import GoldService, gold_service
from .logging_config import LOG_LEVELS, setup_logger
from .predictor import StockPredictor
from .stock_service import StockService, stock_service

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    # 配置加载
    "ConfigLoader",
    "config_loader",
    # 日志
    "setup_logger",
    "LOG_LEVELS",
    # 股票服务
    "StockService",
    "stock_service",
    # 黄金服务
    "GoldService",
    "gold_service",
    # 预测
    "StockPredictor",
    # 飞书推送
    "FeishuNotifier",
    "send_text",
    "send_post",
]
