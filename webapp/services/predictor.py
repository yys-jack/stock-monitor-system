#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票预测服务层
基于技术指标的趋势预测
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class PredictorService:
    """股票预测服务类"""
    
    def __init__(self, stock_code: str = "000063"):
        self.stock_code = stock_code
        self.data = None
    
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
            print(f"[ERROR] 获取历史数据失败：{e}")
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
            
            df['Day'] = range(len(df))
            X = df[['Day']].values
            y = df['收盘'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            last_day = df['Day'].iloc[-1]
            future_days = np.array([[last_day + i] for i in range(1, days + 1)])
            predictions = model.predict(future_days)
            
            r2_score = model.score(X, y)
            confidence = round(r2_score * 100, 2)
            
            trend = "上涨" if predictions[-1] > predictions[0] else "下跌"
            change_pct = ((predictions[-1] - predictions[0]) / predictions[0]) * 100
            
            return {
                "predictions": [round(p, 2) for p in predictions],
                "confidence": confidence,
                "trend": trend,
                "change_pct": round(change_pct, 2),
                "support": round(df['收盘'].min(), 2),
                "resistance": round(df['收盘'].max(), 2),
            }
        except Exception as e:
            print(f"[WARN] 预测失败：{e}")
            return {
                "predictions": [],
                "confidence": 0,
                "trend": "未知",
                "change_pct": 0,
                "support": 0,
                "resistance": 0,
            }
    
    def get_prediction(self) -> Dict:
        """获取预测结果（API 接口）"""
        df = self.fetch_history_data(days=60)
        if df.empty:
            return {"signal": "数据获取失败", "confidence": 0}
        
        df = self.calculate_ma(df)
        df = self.calculate_macd(df)
        df = self.calculate_rsi(df)
        df = self.calculate_kdj(df)
        df = self.calculate_boll(df)
        
        trend_analysis = self.analyze_trend(df)
        prediction = self.predict_price(df, days=5)
        
        return {
            "signal": trend_analysis['overall_signal'],
            "trend": trend_analysis['trend'],
            "confidence": prediction['confidence'],
            "change_pct": prediction['change_pct'],
            "buy_signals": trend_analysis['buy_signals'],
            "sell_signals": trend_analysis['sell_signals'],
            "support": prediction['support'],
            "resistance": prediction['resistance'],
        }
    
    def generate_report(self) -> str:
        """生成预测报告（文本）"""
        df = self.fetch_history_data(days=60)
        if df.empty:
            return "获取数据失败"
        
        df = self.calculate_ma(df)
        df = self.calculate_macd(df)
        df = self.calculate_rsi(df)
        df = self.calculate_kdj(df)
        df = self.calculate_boll(df)
        
        trend_analysis = self.analyze_trend(df)
        prediction = self.predict_price(df, days=5)
        
        latest = df.iloc[-1]
        change_symbol = "🟢" if latest['收盘'] > df.iloc[-2]['收盘'] else "🔴"
        
        report = f"""{change_symbol}【股票预测报告】

💹 当前股价
  收盘价：¥{latest['收盘']:.2f}
  涨跌幅：{latest['涨跌幅']:.2f}%

📊 技术指标
  MA5: ¥{latest['MA5']:.2f} | MA10: ¥{latest['MA10']:.2f}
  MACD: {latest['MACD']:.2f} | RSI: {latest['RSI']:.1f}

🔮 趋势预测
  信号：{trend_analysis['overall_signal']}
  置信度：{prediction['confidence']:.1f}%

📈 关键价位
  支撑位：¥{prediction['support']:.2f}
  压力位：¥{prediction['resistance']:.2f}

⚠️ 风险提示：预测仅供参考，不构成投资建议"""
        
        return report


# 全局实例
predictor_service = PredictorService()
