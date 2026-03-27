#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票预测功能
基于技术分析和机器学习的股票趋势预测
"""

import akshare as ak
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
HISTORY_FILE = PROJECT_ROOT / "data" / "prediction_history.json"

class StockPredictor:
    """股票预测器"""
    
    def __init__(self, stock_code: str = "000063"):
        self.stock_code = stock_code
        self.stock_name = "中兴通讯"
        self.data = None
        self.history = self._load_prediction_history()
    
    def _load_prediction_history(self) -> Dict:
        """加载预测历史记录"""
        if not HISTORY_FILE.exists():
            return {"version": 1, "predictions": []}
        
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] 加载预测历史失败：{e}")
            return {"version": 1, "predictions": []}
    
    def _save_prediction_result(self, prediction_data: Dict):
        """保存预测结果到历史记录"""
        try:
            # 确保 HISTORY_FILE 的目录存在
            HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # 添加时间戳
            prediction_data['predicted_at'] = datetime.now().isoformat()
            prediction_data['stock_code'] = self.stock_code
            prediction_data['stock_name'] = self.stock_name
            
            # 添加到历史记录
            self.history['predictions'].append(prediction_data)
            
            # 限制历史记录数量（最多保留 100 条）
            if len(self.history['predictions']) > 100:
                self.history['predictions'] = self.history['predictions'][-100:]
            
            # 保存到文件
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            
            print(f"[INFO] 预测结果已保存到：{HISTORY_FILE}")
        except Exception as e:
            print(f"[WARN] 保存预测历史失败：{e}")
    
    def _get_historical_accuracy(self) -> Dict:
        """获取该股票的历史预测准确率"""
        stock_predictions = [
            p for p in self.history.get('predictions', [])
            if p.get('stock_code') == self.stock_code
        ]
        
        if not stock_predictions:
            return {"accuracy": 0, "total": 0, "correct": 0, "verified": 0}
        
        # 统计准确率（已验证的预测）
        verified = [p for p in stock_predictions if p.get('actual_trend')]
        if not verified:
            return {"accuracy": 0, "total": len(stock_predictions), "correct": 0, "verified": 0}
        
        correct = sum(1 for p in verified if p.get('predicted_trend') == p.get('actual_trend'))
        
        return {
            "accuracy": correct / len(verified) * 100 if verified else 0,
            "total": len(stock_predictions),
            "correct": correct,
            "verified": len(verified)
        }
    
    def _adjust_confidence_by_history(self, base_confidence: float) -> float:
        """根据历史准确率调整置信度"""
        accuracy_info = self._get_historical_accuracy()
        
        if accuracy_info['verified'] < 5:
            # 历史数据不足，不调整
            return base_confidence
        
        # 根据历史准确率调整置信度
        accuracy_factor = accuracy_info['accuracy'] / 100.0
        
        # 如果历史准确率高，提高置信度；反之降低
        adjusted = base_confidence * (0.8 + 0.4 * accuracy_factor)
        
        # 限制在 30%-95% 之间
        return max(30.0, min(95.0, adjusted))
    
    def fetch_history_data(self, days: int = 60) -> pd.DataFrame:
        """获取历史行情数据"""
        try:
            from akshare import stock_zh_a_hist
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - pd.Timedelta(days=days)).strftime("%Y%m%d")
            
            df = stock_zh_a_hist(
                symbol=self.stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date
            )
            
            self.data = df
            return df
        except Exception as e:
            print(f"❌ 获取历史数据失败：{e}")
            return pd.DataFrame()
    
    def calculate_ma(self, df: pd.DataFrame, windows: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
        """计算均线"""
        for window in windows:
            df[f'MA{window}'] = df['收盘'].rolling(window=window).mean()
        return df
    
    def calculate_macd(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算 MACD 指标"""
        exp1 = df['收盘'].ewm(span=12, adjust=False).mean()
        exp2 = df['收盘'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['Signal']
        return df
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """计算 RSI 指标"""
        delta = df['收盘'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    def calculate_kdj(self, df: pd.DataFrame, n: int = 9) -> pd.DataFrame:
        """计算 KDJ 指标"""
        low_n = df['最低'].rolling(window=n).min()
        high_n = df['最高'].rolling(window=n).max()
        rsv = (df['收盘'] - low_n) / (high_n - low_n) * 100
        df['K'] = rsv.ewm(com=2, adjust=False).mean()
        df['D'] = df['K'].ewm(com=2, adjust=False).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']
        return df
    
    def calculate_boll(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """计算布林带"""
        df['BOLL_Mid'] = df['收盘'].rolling(window=window).mean()
        df['BOLL_Std'] = df['收盘'].rolling(window=window).std()
        df['BOLL_Up'] = df['BOLL_Mid'] + 2 * df['BOLL_Std']
        df['BOLL_Down'] = df['BOLL_Mid'] - 2 * df['BOLL_Std']
        return df
    
    def analyze_trend(self, df: pd.DataFrame) -> Dict:
        """分析趋势"""
        if df.empty or len(df) < 20:
            return {"trend": "数据不足", "signal": "观望"}
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 均线分析
        ma_signal = "中性"
        if latest['MA5'] > latest['MA10'] > latest['MA20']:
            ma_signal = "多头排列"
        elif latest['MA5'] < latest['MA10'] < latest['MA20']:
            ma_signal = "空头排列"
        
        # MACD 分析
        macd_signal = "中性"
        if latest['MACD'] > latest['Signal'] and prev['MACD'] <= prev['Signal']:
            macd_signal = "金叉买入"
        elif latest['MACD'] < latest['Signal'] and prev['MACD'] >= prev['Signal']:
            macd_signal = "死叉卖出"
        
        # RSI 分析
        rsi_signal = "中性"
        if latest['RSI'] > 70:
            rsi_signal = "超买"
        elif latest['RSI'] < 30:
            rsi_signal = "超卖"
        
        # KDJ 分析
        kdj_signal = "中性"
        if latest['K'] > latest['D'] and prev['K'] <= prev['D']:
            kdj_signal = "金叉买入"
        elif latest['K'] < latest['D'] and prev['K'] >= prev['D']:
            kdj_signal = "死叉卖出"
        
        # 综合判断
        buy_signals = sum([
            ma_signal == "多头排列",
            macd_signal == "金叉买入",
            rsi_signal == "超卖",
            kdj_signal == "金叉买入"
        ])
        
        sell_signals = sum([
            ma_signal == "空头排列",
            macd_signal == "死叉卖出",
            rsi_signal == "超买",
            kdj_signal == "死叉卖出"
        ])
        
        if buy_signals >= 3:
            overall_signal = "强烈买入"
        elif buy_signals >= 2:
            overall_signal = "买入"
        elif sell_signals >= 3:
            overall_signal = "强烈卖出"
        elif sell_signals >= 2:
            overall_signal = "卖出"
        else:
            overall_signal = "观望"
        
        return {
            "trend": "上涨" if latest['收盘'] > prev['收盘'] else "下跌",
            "ma_signal": ma_signal,
            "macd_signal": macd_signal,
            "rsi_signal": rsi_signal,
            "kdj_signal": kdj_signal,
            "overall_signal": overall_signal,
            "buy_signals": buy_signals,
            "sell_signals": sell_signals,
        }
    
    def predict_price(self, df: pd.DataFrame, days: int = 5) -> Dict:
        """简单价格预测（线性回归）"""
        try:
            from sklearn.linear_model import LinearRegression
            
            # 准备数据
            df['Day'] = range(len(df))
            X = df[['Day']].values
            y = df['收盘'].values
            
            # 训练模型
            model = LinearRegression()
            model.fit(X, y)
            
            # 预测未来价格
            last_day = df['Day'].iloc[-1]
            future_days = np.array([[last_day + i] for i in range(1, days + 1)])
            predictions = model.predict(future_days)
            
            # 计算置信度
            r2_score = model.score(X, y)
            confidence = round(r2_score * 100, 2)
            
            # 趋势判断
            trend = "上涨" if predictions[-1] > predictions[0] else "下跌"
            change_pct = ((predictions[-1] - predictions[0]) / predictions[0]) * 100
            
            return {
                "predictions": [round(p, 2) for p in predictions],
                "confidence": confidence,
                "trend": trend,
                "change_pct": round(change_pct, 2),
                "support": round(df['收盘'].min(), 2),  # 支撑位
                "resistance": round(df['收盘'].max(), 2),  # 压力位
            }
        except Exception as e:
            print(f"⚠️ 预测失败：{e}")
            return {
                "predictions": [],
                "confidence": 0,
                "trend": "未知",
                "change_pct": 0,
                "support": 0,
                "resistance": 0,
            }
    
    def predict(self) -> Dict:
        """生成预测信号（简化接口）"""
        df = self.fetch_history_data(days=60)
        if df.empty:
            return {"signal": "数据获取失败", "confidence": 0}
        
        # 计算技术指标
        df = self.calculate_ma(df)
        df = self.calculate_macd(df)
        df = self.calculate_rsi(df)
        df = self.calculate_kdj(df)
        df = self.calculate_boll(df)
        
        # 趋势分析
        trend_analysis = self.analyze_trend(df)
        
        # 价格预测
        prediction = self.predict_price(df, days=5)
        
        # 根据历史准确率调整置信度
        base_confidence = prediction['confidence']
        adjusted_confidence = self._adjust_confidence_by_history(base_confidence)
        
        # 获取历史准确率信息
        accuracy_info = self._get_historical_accuracy()
        
        result = {
            "signal": trend_analysis['overall_signal'],
            "trend": trend_analysis['trend'],
            "confidence": adjusted_confidence,
            "base_confidence": base_confidence,  # 原始置信度
            "historical_accuracy": accuracy_info['accuracy'],  # 历史准确率
            "change_pct": prediction['change_pct'],
            "buy_signals": trend_analysis['buy_signals'],
            "sell_signals": trend_analysis['sell_signals'],
            "support": prediction['support'],
            "resistance": prediction['resistance'],
        }
        
        # 保存预测结果到历史记录
        self._save_prediction_result({
            "predicted_trend": trend_analysis['trend'],
            "predicted_signal": trend_analysis['overall_signal'],
            "predicted_confidence": adjusted_confidence,
            "predicted_change_pct": prediction['change_pct'],
            "support_level": prediction['support'],
            "pressure_level": prediction['resistance'],
            # 以下字段在后续验证时填充
            "actual_trend": None,
            "actual_change_pct": None,
            "verified": False,
        })
        
        return result
    
    def generate_report(self) -> str:
        """生成预测报告"""
        print(f"🔮 股票预测报告 - {self.stock_name} ({self.stock_code})")
        print("="*60)
        
        # 获取数据
        df = self.fetch_history_data(days=60)
        if df.empty:
            return "获取数据失败"
        
        # 计算技术指标
        df = self.calculate_ma(df)
        df = self.calculate_macd(df)
        df = self.calculate_rsi(df)
        df = self.calculate_kdj(df)
        df = self.calculate_boll(df)
        
        # 趋势分析
        trend_analysis = self.analyze_trend(df)
        
        # 价格预测
        prediction = self.predict_price(df, days=5)
        
        # 生成报告
        latest = df.iloc[-1]
        report = f"""
📊 技术指标分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
当前价格：¥{latest['收盘']:.2f} ({latest['涨跌幅']:.2f}%)

均线系统：
  MA5:  ¥{latest['MA5']:.2f}
  MA10: ¥{latest['MA10']:.2f}
  MA20: ¥{latest['MA20']:.2f}
  MA60: ¥{latest['MA60']:.2f}
  信号：{trend_analysis['ma_signal']}

MACD 指标：
  MACD: {latest['MACD']:.4f}
  Signal: {latest['Signal']:.4f}
  信号：{trend_analysis['macd_signal']}

RSI 指标：
  RSI(14): {latest['RSI']:.2f}
  信号：{trend_analysis['rsi_signal']}

KDJ 指标：
  K: {latest['K']:.2f}
  D: {latest['D']:.2f}
  J: {latest['J']:.2f}
  信号：{trend_analysis['kdj_signal']}

布林带：
  上轨：¥{latest['BOLL_Up']:.2f}
  中轨：¥{latest['BOLL_Mid']:.2f}
  下轨：¥{latest['BOLL_Down']:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 综合判断
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
买入信号：{trend_analysis['buy_signals']} 个
卖出信号：{trend_analysis['sell_signals']} 个
操作建议：{trend_analysis['overall_signal']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 价格预测（未来 5 日）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
预测趋势：{prediction['trend']}
预计涨幅：{prediction['change_pct']:.2f}%
置信度：{prediction['confidence']:.2f}%

支撑位：¥{prediction['support']:.2f}
压力位：¥{prediction['resistance']:.2f}

预测价格：
"""
        
        for i, price in enumerate(prediction['predictions'], 1):
            report += f"  第{i}日：¥{price:.2f}\n"
        
        report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 预测仅供参考，不构成投资建议
2. 股市有风险，投资需谨慎
3. 建议结合基本面和技术面综合判断
4. 注意设置止损位

📅 报告时间：""" + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(report)
        return report

if __name__ == "__main__":
    predictor = StockPredictor("000063")
    predictor.generate_report()
