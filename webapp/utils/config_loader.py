#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载工具
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 配置文件路径
CONFIG_DIR = PROJECT_ROOT / "config"
STOCKS_CONFIG_FILE = CONFIG_DIR / "stocks_config.json"
GOLD_CONFIG_FILE = CONFIG_DIR / "gold_config.json"
FEISHU_CONFIG_FILE = CONFIG_DIR / "feishu_config.json"


def load_json_config(file_path: Path, default: Optional[Dict] = None) -> Dict[str, Any]:
    """加载 JSON 配置文件"""
    if not file_path.exists():
        if default is not None:
            return default
        return {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 加载配置文件失败 {file_path}: {e}")
        return default or {}


def load_stocks_config() -> Dict[str, Any]:
    """加载股票配置"""
    default = {
        "version": 1,
        "updated_at": "",
        "stocks": [],
        "settings": {
            "push_interval_minutes": 30,
            "alert_threshold_up": 5.0,
            "alert_threshold_down": -5.0,
            "push_format": "single"
        }
    }
    return load_json_config(STOCKS_CONFIG_FILE, default)


def load_gold_config() -> Dict[str, Any]:
    """加载黄金配置"""
    default = {
        "type": "AU9999",
        "alias": "黄金",
        "notes": "上海黄金交易所 AU9999 现货基准价",
        "settings": {
            "push_interval_minutes": 60,
            "retry_times": 3,
            "retry_delay_seconds": 2
        }
    }
    return load_json_config(GOLD_CONFIG_FILE, default)


def load_feishu_config() -> Dict[str, Any]:
    """加载飞书配置"""
    default = {
        "feishu": {
            "enabled": False,
            "user_id": "",
            "app_id": "",
            "app_secret": "",
            "retry_times": 3,
            "retry_delay_seconds": 2
        }
    }
    return load_json_config(FEISHU_CONFIG_FILE, default)


def save_stocks_config(config: Dict[str, Any]) -> bool:
    """保存股票配置"""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(STOCKS_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] 保存股票配置失败：{e}")
        return False


def get_project_root() -> Path:
    """获取项目根目录"""
    return PROJECT_ROOT


def get_config_dir() -> Path:
    """获取配置目录"""
    return CONFIG_DIR
