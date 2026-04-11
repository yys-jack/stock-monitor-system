"""
股票配置管理 API 路由
"""
from datetime import datetime

from fastapi import APIRouter

from app.models.schemas import (
    MessageResponse,
    StockAddRequest,
    StockConfig,
    StocksResponse,
    ToggleResponse,
)
from src import config_loader

router = APIRouter(tags=["Config"])


@router.get("/stocks", response_model=StocksResponse)
async def get_stocks() -> StocksResponse:
    """获取股票配置列表"""
    config = config_loader.load_stocks_config()
    stocks = config.get("stocks", []) if config else []
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
    """添加股票"""
    try:
        code = stock.code.strip()
        name = stock.name.strip()
        market = stock.market.strip()
        alias = stock.alias.strip()
        notes = stock.notes.strip()

        if not code or not name:
            return MessageResponse(success=False, error="股票代码和名称不能为空")

        config = config_loader.load_stocks_config()
        if not config:
            config = {"stocks": [], "settings": {}}

        for s in config.get("stocks", []):
            if s["code"] == code:
                return MessageResponse(success=False, error=f"股票 {code} 已存在")

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

        return MessageResponse(success=True, message=f"已添加股票 {name}({code})", data=new_stock)
    except Exception as e:
        return MessageResponse(success=False, error=str(e))


@router.delete("/stocks/{code}", response_model=MessageResponse)
async def delete_stock(code: str) -> MessageResponse:
    """删除股票"""
    try:
        config = config_loader.load_stocks_config()
        if not config:
            return MessageResponse(success=False, error=f"股票 {code} 不存在")

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
    """切换股票启用状态"""
    try:
        config = config_loader.load_stocks_config()
        if not config:
            return ToggleResponse(success=False, error=f"股票 {code} 不存在")

        found = False
        new_status = False
        for s in config.get("stocks", []):
            if s["code"] == code:
                found = True
                s["enabled"] = not s.get("enabled", True)
                new_status = s["enabled"]
                break

        if not found:
            return ToggleResponse(success=False, error=f"股票 {code} 不存在")

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
