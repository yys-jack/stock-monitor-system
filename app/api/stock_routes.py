"""
股票行情相关 API 路由
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter

from app.models.schemas import (
    HistoryResponse,
    HistoryItem,
    NewsResponse,
    NewsItem,
    OverviewResponse,
    OverviewItem,
    StockResponse,
)
from src import config_loader, stock_service

router = APIRouter(tags=["Stock"])


@router.get("/stock/{code}", response_model=StockResponse)
async def get_stock(code: str) -> StockResponse:
    """获取股票实时数据"""
    stocks = config_loader.load_stocks_config().get("stocks", [])
    stock_info = next((s for s in stocks if s["code"] == code), None)

    if not stock_info:
        stock_info = {"code": code, "name": "Unknown", "market": "sz"}

    price_data = stock_service.fetch_stock_price(code, stock_info.get("market", "sz"))

    if price_data:
        return StockResponse(
            success=True,
            data={
                "stock": stock_info,
                "price": price_data,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        )
    else:
        return StockResponse(
            success=False,
            error="Failed to fetch stock price",
            data={"stock": stock_info},
        )


@router.get("/news/{code}", response_model=NewsResponse)
async def get_news(code: str) -> NewsResponse:
    """获取股票新闻"""
    news_list = stock_service.fetch_news(code)
    news_items = [
        NewsItem(
            title=n.get("title", "")[:80],
            source=n.get("source", "东方财富"),
            date=str(n.get("date", ""))[:16],
            url=n.get("url", ""),
        )
        for n in news_list
    ]
    return NewsResponse(success=True, data=news_items)


@router.get("/history/{code}", response_model=HistoryResponse)
async def get_history(code: str) -> HistoryResponse:
    """获取历史行情"""
    history = stock_service.fetch_history(code)
    history_items = [
        HistoryItem(
            date=h.get("date", ""),
            close=float(h.get("close", 0)),
            change=float(h.get("change", 0)),
        )
        for h in history
    ]
    return HistoryResponse(success=True, data=history_items)


@router.get("/overview", response_model=OverviewResponse)
async def get_overview() -> OverviewResponse:
    """获取股票概览数据"""
    stocks = config_loader.load_stocks_config().get("stocks", [])
    overview = stock_service.fetch_overview(stocks)
    overview_items = [
        OverviewItem(
            code=item["code"],
            name=item["name"],
            alias=item.get("alias", ""),
            current=float(item["current"]),
            change_pct=float(item["change_pct"]),
        )
        for item in overview
    ]
    return OverviewResponse(success=True, data=overview_items)
