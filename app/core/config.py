"""
应用配置管理

使用 Pydantic Settings 进行配置管理
"""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    # 基础配置
    app_name: str = Field("股票监控系统", description="应用名称")
    app_version: str = Field("6.0.0", description="应用版本")
    debug: bool = Field(False, description="调试模式")

    # 服务器配置
    host: str = Field("0.0.0.0", description="监听地址")
    port: int = Field(8000, description="监听端口")

    # CORS 配置
    cors_origins: List[str] = Field(
        ["*"],
        description="允许的源",
    )
    cors_credentials: bool = Field(True, description="是否允许凭证")
    cors_methods: List[str] = Field(["*"], description="允许的方法")
    cors_headers: List[str] = Field(["*"], description="允许的头部")

    # 日志配置
    log_level: str = Field("INFO", description="日志级别")
    log_format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="日志格式",
    )

    # 项目路径
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    config_dir: Path | None = Field(default=None, description="配置目录")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def model_post_init(self, __context):
        """初始化后处理"""
        if self.config_dir is None:
            self.config_dir = self.project_root / "config"


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()


# 全局配置实例
settings = get_settings()
