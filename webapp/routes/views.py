#!/usr/bin/env python3
"""
页面路由模块
"""

from flask import Blueprint, render_template

from src.config_loader import config_loader

views = Blueprint("views", __name__)


@views.route("/")
def index():
    """首页"""
    config = config_loader.load_stocks_config()
    stocks = config.get("stocks", []) if config else []
    default_stock = stocks[0]["code"] if stocks else "000063"
    return render_template("index.html", stocks=stocks, default_stock=default_stock)
