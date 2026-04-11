"""
API 端点 - 兼容层

为旧版 Flask 路由提供兼容的 FastAPI 实现
"""

from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import APIRouter

from app.models.schemas import (
    HistoryResponse,
    HistoryItem,
    NewsResponse,
    NewsItem,
    OverviewResponse,
    OverviewItem,
    PredictReport,
    PredictResponse,
    StockAddRequest,
    StockConfig,
    StockResponse,
    StocksResponse,
    ToggleResponse,
    MessageResponse,
)
from src import config_loader, stock_service
from src.predictor import StockPredictor

router = APIRouter(prefix="/api", tags=["API"])


@router.get("/stock/{code}", response_model=StockResponse)
async def get_stock(code: str) -> StockResponse:
    """
    获取股票实时数据

    - **code**: 股票代码
    """
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
    """
    获取股票新闻

    - **code**: 股票代码
    """
    news_list = stock_service.fetch_news(code)

    # 转换为 Pydantic 模型
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
    """
    获取历史行情

    - **code**: 股票代码
    """
    history = stock_service.fetch_history(code)

    # 转换为 Pydantic 模型
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
    """
    获取股票概览数据
    """
    stocks = config_loader.load_stocks_config().get("stocks", [])
    overview = stock_service.fetch_overview(stocks)

    # 转换为 Pydantic 模型
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


@router.get("/predict/{code}", response_model=PredictResponse)
async def get_predict(code: str) -> PredictResponse:
    """
    获取预测数据

    - **code**: 股票代码
    """
    try:
        predictor = StockPredictor(code)
        result = predictor.predict()

        return PredictResponse(success=True, data=result)
    except Exception as e:
        return PredictResponse(success=False, error=str(e))


@router.get("/predict/report/{code}", response_model=PredictReport)
async def get_predict_report(code: str) -> PredictReport:
    """
    获取预测报告（文本格式）

    - **code**: 股票代码
    """
    try:
        predictor = StockPredictor(code)
        report = predictor.generate_report()

        return PredictReport(success=True, data={"report": report})
    except Exception as e:
        return PredictReport(success=False, error=str(e))


@router.get("/stocks", response_model=StocksResponse)
async def get_stocks() -> StocksResponse:
    """
    获取股票配置列表
    """
    config = config_loader.load_stocks_config()
    stocks = config.get("stocks", []) if config else []

    # 转换为 Pydantic 模型
    stock_configs = [
        StockConfig(
            code=s.get("code", ""),
            name=s.get("name", ""),
            market=s.get("market", "sz"),
            enabled=s.get("enabled", True),
            alias=s.get("alias", ""),
            notes=s.get("notes", ""),
        )
        for s in stocks
    ]

    return StocksResponse(success=True, data=stock_configs)


@router.post("/stocks", response_model=MessageResponse)
async def add_stock(stock: StockAddRequest) -> MessageResponse:
    """
    添加股票

    - **code**: 股票代码
    - **name**: 股票名称
    - **market**: 市场 (sz/sh)
    - **alias**: 别名
    - **notes**: 备注
    """
    try:
        code = stock.code.strip()
        name = stock.name.strip()
        market = stock.market.strip()
        alias = stock.alias.strip()
        notes = stock.notes.strip()

        if not code or not name:
            return MessageResponse(
                success=False, error="股票代码和名称不能为空"
            )

        config = config_loader.load_stocks_config()
        if not config:
            config = {"stocks": [], "settings": {}}

        # 检查是否已存在
        for s in config.get("stocks", []):
            if s["code"] == code:
                return MessageResponse(
                    success=False, error=f"股票 {code} 已存在"
                )

        # 添加新股票
        new_stock = {
            "code": code,
            "name": name,
            "market": market,
            "enabled": True,
            "alias": alias or name,
            "notes": notes,
        }
        config["stocks"].append(new_stock)
        config["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        config["version"] = config.get("version", 1) + 1

        if not config_loader.save_config("stocks_config.json", config):
            return MessageResponse(success=False, error="保存配置失败")

        return MessageResponse(
            success=True,
            message=f"已添加股票 {name}({code})",
            data=new_stock,
        )
    except Exception as e:
        return MessageResponse(success=False, error=str(e))


@router.delete("/stocks/{code}", response_model=MessageResponse)
async def delete_stock(code: str) -> MessageResponse:
    """
    删除股票

    - **code**: 股票代码
    """
    try:
        config = config_loader.load_stocks_config()
        if not config:
            return MessageResponse(success=False, error=f"股票 {code} 不存在")

        # 查找并删除
        found = False
        new_stocks = []
        for s in config.get("stocks", []):
            if s["code"] == code:
                found = True
            else:
                new_stocks.append(s)

        if not found:
            return MessageResponse(success=False, error=f"股票 {code} 不存在")

        config["stocks"] = new_stocks
        config["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        config["version"] = config.get("version", 1) + 1

        if not config_loader.save_config("stocks_config.json", config):
            return MessageResponse(success=False, error="保存配置失败")

        return MessageResponse(success=True, message=f"已删除股票 {code}")
    except Exception as e:
        return MessageResponse(success=False, error=str(e))


@router.post("/stocks/{code}/toggle", response_model=ToggleResponse)
async def toggle_stock(code: str) -> ToggleResponse:
    """
    切换股票启用状态

    - **code**: 股票代码
    """
    try:
        config = config_loader.load_stocks_config()
        if not config:
            return ToggleResponse(
                success=False, error=f"股票 {code} 不存在"
            )

        found = False
        new_status = False
        for s in config.get("stocks", []):
            if s["code"] == code:
                found = True
                s["enabled"] = not s.get("enabled", True)
                new_status = s["enabled"]
                break

        if not found:
            return ToggleResponse(
                success=False, error=f"股票 {code} 不存在"
            )

        config["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        config["version"] = config.get("version", 1) + 1

        if not config_loader.save_config("stocks_config.json", config):
            return ToggleResponse(success=False, error="保存配置失败")

        return ToggleResponse(
            success=True,
            data={"enabled": new_status},
            message=f"股票 {code} 已{'启用' if new_status else '禁用'}",
        )
    except Exception as e:
        return ToggleResponse(success=False, error=str(e))
