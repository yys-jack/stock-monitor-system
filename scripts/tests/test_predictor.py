#!/usr/bin/env python3
"""
股票预测器测试
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pandas as pd

from src.predictor import StockPredictor


class TestStockPredictor(unittest.TestCase):
    """股票预测器测试类"""

    def setUp(self):
        """测试前准备"""
        self.predictor = StockPredictor("000063")

    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.predictor.stock_code, "000063")
        self.assertIsNotNone(self.predictor.project_root)
        self.assertIsNotNone(self.predictor.history_file)

    def test_calculate_ma(self):
        """测试计算均线"""
        # 创建模拟数据
        df = pd.DataFrame({"收盘": [10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 11.8, 12.0]})

        # 计算均线
        df = self.predictor.calculate_ma(df, windows=[3, 5])

        # 验证均线列存在
        self.assertIn("MA3", df.columns)
        self.assertIn("MA5", df.columns)

        # 验证 MA3 值（3 日均线）- 最后 3 个值的平均
        self.assertAlmostEqual(df["MA3"].iloc[-1], (11.5 + 11.8 + 12.0) / 3, places=2)

    def test_calculate_macd(self):
        """测试计算 MACD 指标"""
        df = pd.DataFrame({"收盘": [10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 11.8, 12.0]})

        df = self.predictor.calculate_macd(df)

        # 验证 MACD 列存在
        self.assertIn("MACD", df.columns)
        self.assertIn("Signal", df.columns)
        self.assertIn("MACD_Hist", df.columns)

    def test_calculate_rsi(self):
        """测试计算 RSI 指标"""
        df = pd.DataFrame({"收盘": [10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 11.8, 12.0]})

        df = self.predictor.calculate_rsi(df, period=6)

        # 验证 RSI 列存在
        self.assertIn("RSI", df.columns)

        # RSI 值应在 0-100 之间
        rsi_values = df["RSI"].dropna()
        if len(rsi_values) > 0:
            self.assertTrue(all(0 <= rsi <= 100 for rsi in rsi_values))

    def test_calculate_kdj(self):
        """测试计算 KDJ 指标"""
        df = pd.DataFrame(
            {
                "收盘": [10.0, 10.5, 11.0, 10.8, 11.2],
                "最高": [10.2, 10.8, 11.2, 11.0, 11.5],
                "最低": [9.8, 10.2, 10.8, 10.5, 11.0],
            }
        )

        df = self.predictor.calculate_kdj(df, n=3)

        # 验证 KDJ 列存在
        self.assertIn("K", df.columns)
        self.assertIn("D", df.columns)
        self.assertIn("J", df.columns)

    def test_calculate_boll(self):
        """测试计算布林带"""
        df = pd.DataFrame({"收盘": [10.0, 10.5, 11.0, 10.8, 11.2, 11.5, 11.8, 12.0]})

        df = self.predictor.calculate_boll(df, window=5)

        # 验证布林带列存在
        self.assertIn("BOLL_Mid", df.columns)
        self.assertIn("BOLL_Std", df.columns)
        self.assertIn("BOLL_Up", df.columns)
        self.assertIn("BOLL_Down", df.columns)

    def test_analyze_trend_empty_data(self):
        """测试空数据分析"""
        df = pd.DataFrame()
        result = self.predictor.analyze_trend(df)

        self.assertEqual(result["trend"], "数据不足")
        self.assertEqual(result["signal"], "观望")

    def test_analyze_trend_insufficient_data(self):
        """测试数据不足情况"""
        df = pd.DataFrame({"收盘": [10.0, 10.5]})
        result = self.predictor.analyze_trend(df)

        self.assertEqual(result["trend"], "数据不足")
        self.assertEqual(result["signal"], "观望")

    def test_predict_price(self):
        """测试价格预测"""
        df = pd.DataFrame(
            {
                "收盘": [10.0, 10.2, 10.5, 10.3, 10.8, 11.0, 11.2, 11.5, 11.3, 11.8],
                "Day": range(10),
            }
        )

        result = self.predictor.predict_price(df, days=5)

        # 验证返回格式
        self.assertIn("predictions", result)
        self.assertIn("confidence", result)
        self.assertIn("trend", result)
        self.assertIn("change_pct", result)
        self.assertIn("support", result)
        self.assertIn("resistance", result)

    def test_historical_accuracy_empty(self):
        """测试空历史准确率"""
        accuracy_info = self.predictor._get_historical_accuracy()

        self.assertIn("accuracy", accuracy_info)
        self.assertIn("total", accuracy_info)
        self.assertIn("correct", accuracy_info)
        self.assertIn("verified", accuracy_info)

    def test_adjust_confidence_no_history(self):
        """测试无历史记录时的置信度调整"""
        base_confidence = 70.0
        adjusted = self.predictor._adjust_confidence_by_history(base_confidence)

        # 无历史记录时应返回原值
        self.assertEqual(adjusted, base_confidence)

    def test_predict_result_format(self):
        """测试预测结果格式"""
        # 使用 mock 避免实际网络请求
        with patch.object(self.predictor, "fetch_history_data") as mock_fetch:
            mock_df = pd.DataFrame(
                {
                    "收盘": [10.0 + i * 0.1 for i in range(60)],
                    "最高": [10.2 + i * 0.1 for i in range(60)],
                    "最低": [9.8 + i * 0.1 for i in range(60)],
                }
            )
            mock_fetch.return_value = mock_df

            result = self.predictor.predict()

            # 验证返回格式
            self.assertIn("signal", result)
            self.assertIn("trend", result)
            self.assertIn("confidence", result)


if __name__ == "__main__":
    unittest.main()
