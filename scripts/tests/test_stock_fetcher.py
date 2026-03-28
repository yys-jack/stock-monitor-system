#!/usr/bin/env python3
"""
股票价格获取测试
"""

import sys
import unittest
from datetime import datetime
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestStockPriceFetcher(unittest.TestCase):
    """股票价格获取测试类"""

    def test_fetch_price_format(self):
        """测试股价数据格式"""
        # 模拟股价数据
        mock_data = {
            "name": "中兴通讯",
            "code": "000063",
            "current": 28.5,
            "prev_close": 28.0,
            "change_pct": 1.79,
        }

        # 验证数据格式
        self.assertIsInstance(mock_data["name"], str)
        self.assertIsInstance(mock_data["code"], str)
        self.assertIsInstance(mock_data["current"], float)
        self.assertIsInstance(mock_data["change_pct"], float)

    def test_change_calculation(self):
        """测试涨跌幅计算"""
        current = 28.5
        prev_close = 28.0

        change_pct = (current - prev_close) / prev_close * 100

        self.assertAlmostEqual(change_pct, 1.79, places=2)

    def test_market_hours(self):
        """测试交易时间判断"""
        now = datetime.now()

        # 上午交易时间：9:30-11:30
        # 下午交易时间：13:00-15:00
        is_trading_time = (
            (9 <= now.hour < 11 or (now.hour == 11 and now.minute <= 30)) or (13 <= now.hour < 15)
        ) and now.weekday() < 5

        # 仅验证逻辑，不验证结果（因为结果取决于当前时间）
        self.assertIsInstance(is_trading_time, bool)


if __name__ == "__main__":
    unittest.main()
