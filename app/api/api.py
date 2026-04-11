"""
API 端点 - 路由聚合

将所有路由模块聚合到统一的 /api 前缀下
"""
from fastapi import APIRouter

from app.api.stock_routes import router as stock_router
from app.api.predict_routes import router as predict_router
from app.api.config_routes import router as config_router

# 创建主路由
api_router = APIRouter(prefix="/api", tags=["API"])

# 包含子路由
api_router.include_router(stock_router)
api_router.include_router(predict_router)
api_router.include_router(config_router)
