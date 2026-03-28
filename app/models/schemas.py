"""
Pydantic 数据模型定义

用于 API 请求/响应的数据验证和序列化
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class StockPriceData(BaseModel):
    """股票价格数据"""

    name: str = Field(..., description="股票名称")
    code: str = Field(..., description="股票代码")
    current: float = Field(..., description="当前价格")
    prev_close: float = Field(..., description="昨收价")
    open: float = Field(..., description="开盘价")
    volume: int = Field(..., description="成交量")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    change_amt: float = Field(..., description="涨跌额")
    change_pct: float = Field(..., description="涨跌幅")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "中兴通讯",
                "code": "000063",
                "current": 28.5,
                "prev_close": 28.0,
                "open": 28.2,
                "volume": 12345678,
                "high": 29.0,
                "low": 27.8,
                "change_amt": 0.5,
                "change_pct": 1.79,
            }
        }
    )


class StockResponse(BaseModel):
    """股票实时数据响应"""

    success: bool = Field(True, description="请求是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="响应数据")
    error: Optional[str] = Field(None, description="错误信息")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": {
                    "stock": {"code": "000063", "name": "中兴通讯", "market": "sz"},
                    "price": {
                        "name": "中兴通讯",
                        "code": "000063",
                        "current": 28.5,
                        "change_pct": 1.79,
                    },
                    "update_time": "2026-03-29 15:00:00",
                },
            }
        }
    )


class NewsItem(BaseModel):
    """新闻条目"""

    title: str = Field(..., description="新闻标题")
    source: str = Field(..., description="文章来源")
    date: str = Field(..., description="发布时间")
    url: str = Field(..., description="新闻链接")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "中兴通讯发布最新财报",
                "source": "东方财富",
                "date": "2026-03-29 10:30",
                "url": "https://example.com/news/123",
            }
        }
    )


class NewsResponse(BaseModel):
    """新闻列表响应"""

    success: bool = Field(True, description="请求是否成功")
    data: List[NewsItem] = Field(default_factory=list, description="新闻列表")
    error: Optional[str] = Field(None, description="错误信息")


class HistoryItem(BaseModel):
    """历史行情条目"""

    date: str = Field(..., description="日期")
    close: float = Field(..., description="收盘价")
    change: float = Field(..., description="涨跌幅")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2026-03-29",
                "close": 28.5,
                "change": 1.79,
            }
        }
    )


class HistoryResponse(BaseModel):
    """历史行情响应"""

    success: bool = Field(True, description="请求是否成功")
    data: List[HistoryItem] = Field(default_factory=list, description="历史数据")
    error: Optional[str] = Field(None, description="错误信息")


class OverviewItem(BaseModel):
    """股票概览条目"""

    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    alias: str = Field("", description="别名")
    current: float = Field(..., description="当前价格")
    change_pct: float = Field(..., description="涨跌幅")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "000063",
                "name": "中兴通讯",
                "alias": "中兴",
                "current": 28.5,
                "change_pct": 1.79,
            }
        }
    )


class OverviewResponse(BaseModel):
    """概览数据响应"""

    success: bool = Field(True, description="请求是否成功")
    data: List[OverviewItem] = Field(default_factory=list, description="概览数据")
    error: Optional[str] = Field(None, description="错误信息")


class PredictResponse(BaseModel):
    """预测数据响应"""

    success: bool = Field(True, description="请求是否成功")
    data: Optional[Dict[str, Any]] = Field(None, description="预测数据")
    error: Optional[str] = Field(None, description="错误信息")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": {
                    "signal": "买入",
                    "trend": "上涨",
                    "confidence": 75.5,
                    "change_pct": 2.5,
                    "buy_signals": 3,
                    "sell_signals": 1,
                    "support": 27.0,
                    "resistance": 30.0,
                },
            }
        }
    )


class PredictReport(BaseModel):
    """预测报告响应"""

    success: bool = Field(True, description="请求是否成功")
    data: Dict[str, str] = Field(default_factory=dict, description="报告数据")
    error: Optional[str] = Field(None, description="错误信息")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": {"report": "📊 技术指标分析..."},
            }
        }
    )


class StockConfig(BaseModel):
    """股票配置"""

    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    market: str = Field("sz", description="市场")
    enabled: bool = Field(True, description="是否启用")
    alias: str = Field("", description="别名")
    notes: str = Field("", description="备注")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "000063",
                "name": "中兴通讯",
                "market": "sz",
                "enabled": True,
                "alias": "中兴",
                "notes": "5G 龙头",
            }
        }
    )


class StocksResponse(BaseModel):
    """股票配置列表响应"""

    success: bool = Field(True, description="请求是否成功")
    data: List[StockConfig] = Field(default_factory=list, description="股票列表")
    error: Optional[str] = Field(None, description="错误信息")


class StockAddRequest(BaseModel):
    """添加股票请求"""

    code: str = Field(..., description="股票代码")
    name: str = Field(..., description="股票名称")
    market: str = Field("sz", description="市场")
    alias: str = Field("", description="别名")
    notes: str = Field("", description="备注")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "000063",
                "name": "中兴通讯",
                "market": "sz",
                "alias": "中兴",
                "notes": "5G 龙头",
            }
        }
    )


class ToggleResponse(BaseModel):
    """切换状态响应"""

    success: bool = Field(True, description="请求是否成功")
    data: Dict[str, bool] = Field(default_factory=dict, description="状态数据")
    message: str = Field("", description="消息")
    error: Optional[str] = Field(None, description="错误信息")


class MessageResponse(BaseModel):
    """通用消息响应"""

    success: bool = Field(True, description="请求是否成功")
    message: str = Field("", description="消息")
    data: Optional[Dict[str, Any]] = Field(None, description="数据")
    error: Optional[str] = Field(None, description="错误信息")


# 通用 API 响应类型
ApiResponse = (
    StockResponse | NewsResponse | HistoryResponse | OverviewResponse | PredictResponse
)
