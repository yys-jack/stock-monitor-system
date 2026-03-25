#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页面路由模块
"""

from flask import Blueprint, render_template
from webapp.utils.config_loader import load_stocks_config

views = Blueprint('views', __name__)


@views.route('/')
def index():
    """首页"""
    stocks = load_stocks_config().get('stocks', [])
    default_stock = stocks[0]['code'] if stocks else "000063"
    return render_template('index.html', stocks=stocks, default_stock=default_stock)
