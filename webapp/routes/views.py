#!/usr/bin/env python3
"""
页面路由模块
"""

import sys
from pathlib import Path

from flask import Blueprint, render_template

# 添加 src 到路径
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from src.config_loader import config_loader

views = Blueprint("views", __name__)


@views.route("/")
def index():
    """首页"""
    config = config_loader.load_stocks_config()
    stocks = config.get("stocks", []) if config else []
    default_stock = stocks[0]["code"] if stocks else "000063"
    return render_template("index.html", stocks=stocks, default_stock=default_stock)
