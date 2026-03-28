"""
页面视图路由

提供 HTML 页面渲染
"""

from pathlib import Path
from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services import config_loader

router = APIRouter(tags=["Views"])

# 模板配置 - 使用绝对路径
template_path = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(template_path))


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request) -> HTMLResponse:
    """
    首页

    显示股票监控仪表板
    """
    config = config_loader.load_stocks_config()
    stocks: List[dict] = config.get("stocks", []) if config else []
    default_stock = stocks[0]["code"] if stocks else "000063"

    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "stocks": stocks,
            "default_stock": default_stock,
        },
    )


@router.get("/stock/{code}", response_class=HTMLResponse, include_in_schema=False)
async def stock_detail(request: Request, code: str) -> HTMLResponse:
    """
    股票详情页

    - **code**: 股票代码
    """
    config = config_loader.load_stocks_config()
    stocks: List[dict] = config.get("stocks", []) if config else []

    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "stocks": stocks,
            "default_stock": code,
        },
    )
