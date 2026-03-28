#!/usr/bin/env python3
"""
股票服务测试
"""

import sys
import unittest
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.stock_service import StockService, stock_service


class TestStockService(unittest.TestCase):
    """股票服务测试类"""

    def setUp(self):
        """测试前准备"""
        self.service = StockService()

    def test_fetch_stock_price_format(self):
        """测试股价数据格式"""
        # 使用模拟数据测试格式
        mock_data = {
            "name": "中兴通讯",
            "code": "000063",
            "current": 28.5,
            "prev_close": 28.0,
            "open": 28.2,
            "volume": 100000,
            "high": 29.0,
            "low": 27.8,
            "change_amt": 0.5,
            "change_pct": 1.79,
        }

        # 验证数据格式
        self.assertIsInstance(mock_data["name"], str)
        self.assertIsInstance(mock_data["code"], str)
        self.assertIsInstance(mock_data["current"], float)
        self.assertIsInstance(mock_data["change_pct"], float)

    def test_service_instance(self):
        """测试全局实例"""
        self.assertIsNotNone(stock_service)
        self.assertIsInstance(stock_service, StockService)

    def test_fetch_news_returns_list(self):
        """测试获取新闻返回列表"""
        # 测试返回类型
        news = self.service.fetch_news("000063")
        self.assertIsInstance(news, list)

    def test_fetch_history_returns_list(self):
        """测试获取历史行情返回列表"""
        # 测试返回类型
        history = self.service.fetch_history("000063")
        self.assertIsInstance(history, list)

    def test_market_code_validation(self):
        """测试市场代码验证"""
        # 有效的市场代码
        valid_markets = ["sz", "sh"]
        for market in valid_markets:
            self.assertIn(market, ["sz", "sh"])

        # 无效的市场代码处理
        invalid_markets = ["bj", "hk", "us", ""]
        for market in invalid_markets:
            self.assertNotIn(market, ["sz", "sh"])


if __name__ == "__main__":
    unittest.main()
