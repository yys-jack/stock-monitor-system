"""
FastAPI 应用主文件

股票监控系统 Web 应用入口
"""

import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app import __version__
from app.api import api_router, views_router
from app.core import settings, RequestLoggingMiddleware
from app.core.config import Settings


def setup_logging(log_level: str, log_format: str) -> None:
    """配置日志"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    formatter = logging.Formatter(log_format)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # 根日志
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    # UVicorn 日志
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = []
    uvicorn_logger.addHandler(console_handler)


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用

    使用工厂模式创建和配置应用实例
    """
    # 加载配置
    app_settings = settings

    # 配置日志
    setup_logging(app_settings.log_level, app_settings.log_format)

    # 创建应用
    app = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        description="基于 FastAPI 的股票监控系统 - 提供实时股价、新闻、历史行情和预测功能",
        docs_url="/docs",  # Swagger UI
        redoc_url="/redoc",  # ReDoc
        openapi_url="/openapi.json",
    )

    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_origins,
        allow_credentials=app_settings.cors_credentials,
        allow_methods=app_settings.cors_methods,
        allow_headers=app_settings.cors_headers,
    )

    # 添加请求日志中间件
    app.add_middleware(RequestLoggingMiddleware)

    # 注册路由
    app.include_router(views_router)  # 页面视图
    app.include_router(api_router)  # API 接口

    # 挂载静态文件
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # 根路径重定向到文档
    @app.get("/redirect-to-docs", include_in_schema=False)
    async def redirect_to_docs():
        """重定向到 API 文档"""
        return RedirectResponse(url="/docs")

    # 健康检查
    @app.get("/health", tags=["Health"])
    async def health_check():
        """健康检查端点"""
        return {"status": "healthy", "version": __version__}

    # 错误处理
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        """404 错误处理"""
        return {"success": False, "error": "Not Found"}

    @app.exception_handler(500)
    async def internal_error_handler(request, exc):
        """500 错误处理"""
        return {"success": False, "error": "Internal Server Error"}

    return app


# 创建应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    print("🦞 股票监控系统 Web 界面启动 (FastAPI)")
    print("=" * 60)
    print(f"API 文档：http://localhost:{settings.port}/docs")
    print(f"首页：http://localhost:{settings.port}/")
    print("=" * 60)

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
