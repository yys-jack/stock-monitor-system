#!/usr/bin/env python3
"""
统一配置加载器
提供配置加载、验证和缓存功能
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigLoader:
    """配置加载器类"""

    _cache: Dict[str, Any] = {}
    _cache_time: Dict[str, datetime] = {}

    def __init__(self, project_root: Optional[Path] = None):
        """
        初始化配置加载器

        Args:
            project_root: 项目根目录，默认为当前文件的父目录的父目录
        """
        self.project_root = project_root or Path(__file__).parent.parent
        self.config_dir = self.project_root / "config"

    def load_json(
        self, filename: str, use_cache: bool = True, cache_ttl_seconds: int = 60
    ) -> Optional[Dict]:
        """
        加载 JSON 配置文件

        Args:
            filename: 文件名
            use_cache: 是否使用缓存
            cache_ttl_seconds: 缓存有效期（秒）

        Returns:
            配置字典，加载失败返回 None
        """
        cache_key = str(self.config_dir / filename)

        # 检查缓存
        if use_cache and cache_key in self._cache:
            cache_age = (datetime.now() - self._cache_time[cache_key]).total_seconds()
            if cache_age < cache_ttl_seconds:
                return self._cache[cache_key]

        # 加载文件
        filepath = self.config_dir / filename
        if not filepath.exists():
            # 尝试加载示例文件
            example_file = self.config_dir / f"{filename.replace('.json', '')}.example.json"
            if example_file.exists():
                filepath = example_file
            else:
                return None

        try:
            with open(filepath, encoding="utf-8") as f:
                config = json.load(f)

            # 更新缓存
            if use_cache:
                self._cache[cache_key] = config
                self._cache_time[cache_key] = datetime.now()

            return config
        except Exception as e:
            print(f"[ERROR] 加载配置文件失败 {filename}: {e}")
            return None

    def load_stocks_config(self) -> Optional[Dict]:
        """加载股票配置"""
        return self.load_json("stocks_config.json")

    def load_feishu_config(self) -> Optional[Dict]:
        """加载飞书配置"""
        config = self.load_json("feishu_config.json")
        if config:
            return config.get("feishu", {})
        return None

    def load_gold_config(self) -> Optional[Dict]:
        """加载黄金配置"""
        return self.load_json("gold_config.json")

    def save_config(self, filename: str, data: Dict) -> bool:
        """
        保存配置到文件

        Args:
            filename: 文件名
            data: 配置数据

        Returns:
            是否保存成功
        """
        filepath = self.config_dir / filename

        try:
            # 确保目录存在
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # 清除缓存
            cache_key = str(filepath)
            if cache_key in self._cache:
                del self._cache[cache_key]

            return True
        except Exception as e:
            print(f"[ERROR] 保存配置文件失败 {filename}: {e}")
            return False

    def get_env(self, key: str, default: str = "") -> str:
        """获取环境变量"""
        return os.environ.get(key, default)

    def get_env_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔型环境变量"""
        value = os.environ.get(key, "").lower()
        if value in ("true", "1", "yes"):
            return True
        if value in ("false", "0", "no"):
            return False
        return default


# 全局配置加载器实例
config_loader = ConfigLoader()
