#!/usr/bin/env python3
"""
黄金服务测试
"""

import sys
import unittest
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.gold_service import GoldService, gold_service


class TestGoldService(unittest.TestCase):
    """黄金服务测试类"""

    def setUp(self):
        """测试前准备"""
        self.service = GoldService()

    def test_format_price_message(self):
        """测试格式化价格消息"""
        gold_data = {
            "source": "SHFE",
            "symbol": "AU2606",
            "current_cny_g": 620.5,
            "spot_cny_g": 617.0,
            "current_usd_oz": 2680.5,
            "change_cny_g": 3.5,
            "change_pct": 0.57,
            "update_time": "2026-03-28 10:30:00",
        }

        message = self.service.format_price_message(gold_data)

        # 验证消息格式
        self.assertIsInstance(message, str)
        self.assertIn("AU2606", message)
        self.assertIn("620.5", message)
        self.assertIn("元/克", message)

    def test_format_price_message_with_negative_change(self):
        """测试格式化负涨幅消息"""
        gold_data = {
            "source": "SHFE",
            "symbol": "AU2606",
            "current_cny_g": 615.0,
            "spot_cny_g": 611.5,
            "current_usd_oz": 2650.0,
            "change_cny_g": -5.5,
            "change_pct": -0.89,
            "update_time": "2026-03-28 10:30:00",
        }

        message = self.service.format_price_message(gold_data)

        self.assertIsInstance(message, str)
        self.assertIn("📉", message)  # 下跌图标

    def test_format_price_message_with_zero_change(self):
        """测试格式化零涨幅消息"""
        gold_data = {
            "source": "SHFE",
            "symbol": "AU2606",
            "current_cny_g": 618.0,
            "spot_cny_g": 614.5,
            "current_usd_oz": 2665.0,
            "change_cny_g": 0.0,
            "change_pct": 0.0,
            "update_time": "2026-03-28 10:30:00",
        }

        message = self.service.format_price_message(gold_data)

        self.assertIsInstance(message, str)
        self.assertIn("➡️", message)  # 持平图标

    def test_service_instance(self):
        """测试全局实例"""
        self.assertIsNotNone(gold_service)
        self.assertIsInstance(gold_service, GoldService)

    def test_gold_data_keys(self):
        """测试黄金数据键名"""
        required_keys = [
            "source",
            "symbol",
            "current_cny_g",
            "spot_cny_g",
            "current_usd_oz",
            "change_cny_g",
            "change_pct",
        ]

        sample_data = {
            "source": "SHFE",
            "symbol": "AU2606",
            "current_cny_g": 620.5,
            "spot_cny_g": 617.0,
            "current_usd_oz": 2680.5,
            "change_cny_g": 3.5,
            "change_pct": 0.57,
        }

        for key in required_keys:
            self.assertIn(key, sample_data)


if __name__ == "__main__":
    unittest.main()
