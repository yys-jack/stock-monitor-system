#!/usr/bin/env python3
"""
股票服务层
负责股票数据获取和处理
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import pandas as pd
import requests


class StockService:
    """股票服务类"""

    def __init__(self):
        self.base_url = "https://qt.gtimg.cn/q"

    def fetch_stock_price(self, code: str, market: str = "sz") -> Optional[Dict[str, Any]]:
        """
        获取股票实时价格

        Args:
            code: 股票代码
            market: 市场 (sz/sh)

        Returns:
            股票价格数据字典，失败返回 None
        """
        try:
            url = f"{self.base_url}={market}{code}"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }

            resp = requests.get(url, headers=headers, timeout=10)
            resp.encoding = "gbk"  # 腾讯财经返回 GBK 编码

            if resp.status_code != 200:
                return None

            content = resp.text.strip()
            if not content.startswith("v_"):
                return None

            # 解析数据
            data_str = content.split('="')[1].rstrip('";')
            fields = data_str.split("~")

            if len(fields) < 35:
                return None

            return {
                "name": fields[1],
                "code": fields[2],
                "current": float(fields[3]) if fields[3] else 0,
                "prev_close": float(fields[4]) if fields[4] else 0,
                "open": float(fields[5]) if fields[5] else 0,
                "volume": int(fields[6]) if fields[6] else 0,
                "high": float(fields[33]) if fields[33] else 0,
                "low": float(fields[34]) if fields[34] else 0,
                "change_amt": float(fields[31]) if fields[31] else 0,
                "change_pct": float(fields[32]) if fields[32] else 0,
            }

        except Exception as e:
            print(f"[ERROR] 获取{code}股价失败：{e}")
            return None

    def fetch_news(self, code: str, limit: int = 10) -> List[Dict[str, str]]:
        """获取股票新闻"""
        try:
            import akshare as ak

            news_df = ak.stock_news_em(symbol=code)

            if len(news_df) == 0:
                return []

            news_list = []
            for _, row in news_df.head(limit).iterrows():
                news_list.append(
                    {
                        "title": row.get("新闻标题", "")[:80],
                        "source": row.get("文章来源", "东方财富"),
                        "date": str(row.get("发布时间", ""))[:16],
                        "url": row.get("新闻链接", ""),
                    }
                )

            return news_list

        except Exception as e:
            print(f"[ERROR] 获取新闻失败：{e}")
            return []

    def fetch_history(self, code: str, days: int = 30) -> List[Dict[str, Any]]:
        """获取历史行情"""
        try:
            from akshare import stock_zh_a_hist

            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - pd.Timedelta(days=days)).strftime("%Y%m%d")

            df = stock_zh_a_hist(
                symbol=code, period="daily", start_date=start_date, end_date=end_date
            )

            if len(df) == 0:
                return []

            history = []
            for _, row in df.tail(days).iterrows():
                history.append(
                    {
                        "date": str(row.get("日期", "")),
                        "close": float(row.get("收盘", 0)),
                        "change": float(row.get("涨跌幅", 0)),
                    }
                )

            return history

        except Exception as e:
            print(f"[ERROR] 获取历史行情失败：{e}")
            return []

    def fetch_overview(self, stocks: List[Dict]) -> List[Dict[str, Any]]:
        """获取股票概览"""
        overview = []

        for stock in stocks:
            if not stock.get("enabled", True):
                continue

            code = stock["code"]
            market = stock.get("market", "sz")
            price_data = self.fetch_stock_price(code, market)

            if price_data:
                overview.append(
                    {
                        "code": code,
                        "name": stock["name"],
                        "alias": stock.get("alias", ""),
                        "current": price_data["current"],
                        "change_pct": price_data["change_pct"],
                    }
                )

        return overview


# 全局实例
stock_service = StockService()
