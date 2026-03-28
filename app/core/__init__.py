"""
FastAPI 应用核心配置模块

包含应用配置、CORS、中间件等
"""

from .config import settings
from .middleware import RequestLoggingMiddleware

__all__ = ["settings", "RequestLoggingMiddleware"]
