"""
请求日志中间件

记录所有 HTTP 请求的详细信息
"""

import logging
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    def __init__(self, app, logger: logging.Logger = None):
        super().__init__(app)
        self.logger = logger or logging.getLogger("uvicorn.request")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""
        # 记录请求开始
        start_time = time.time()

        # 获取请求信息
        method = request.method
        path = request.url.path
        client = request.client.host if request.client else "unknown"
        query = str(request.url.query) if request.url.query else ""

        # 构建请求日志
        log_parts = [
            f"{client}",
            f'"{method} {path}{f"?{query}" if query else ""}"',
        ]

        try:
            # 执行请求
            response = await call_next(request)

            # 计算处理时间
            process_time = time.time() - start_time

            # 记录响应信息
            self.logger.info(
                "%s - %s - %s - %.3fs",
                method,
                path,
                response.status_code,
                process_time,
            )

            # 添加处理时间头
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # 记录错误
            process_time = time.time() - start_time
            self.logger.error(
                "%s - %s - Error: %s - %.3fs",
                method,
                path,
                str(e),
                process_time,
            )
            raise
