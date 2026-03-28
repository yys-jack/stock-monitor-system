#!/usr/bin/env python3
"""
API 路由模块
"""

from datetime import datetime

from flask import Blueprint, jsonify, request

from src.config_loader import config_loader
from src.predictor import StockPredictor
from src.stock_service import stock_service

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/stock/<code>", methods=["GET"])
def get_stock(code):
    """获取股票实时数据"""
    stocks = (
        config_loader.load_stocks_config().get("stocks", [])
        if config_loader.load_stocks_config()
        else []
    )
    stock_info = next((s for s in stocks if s["code"] == code), None)

    if not stock_info:
        stock_info = {"code": code, "name": "Unknown", "market": "sz"}

    price_data = stock_service.fetch_stock_price(code, stock_info.get("market", "sz"))

    if price_data:
        return jsonify(
            {
                "success": True,
                "data": {
                    "stock": stock_info,
                    "price": price_data,
                    "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            }
        )
    else:
        return jsonify({"success": False, "error": "Failed to fetch stock price"}), 500


@api.route("/news/<code>", methods=["GET"])
def get_news(code):
    """获取新闻"""
    news_list = stock_service.fetch_news(code)
    return jsonify({"success": True, "data": news_list})


@api.route("/history/<code>", methods=["GET"])
def get_history(code):
    """获取历史行情"""
    history = stock_service.fetch_history(code)
    return jsonify({"success": True, "data": history})


@api.route("/overview", methods=["GET"])
def get_overview():
    """获取概览数据"""
    stocks = (
        config_loader.load_stocks_config().get("stocks", [])
        if config_loader.load_stocks_config()
        else []
    )
    overview = stock_service.fetch_overview(stocks)

    return jsonify({"success": True, "data": overview})


@api.route("/predict/<code>", methods=["GET"])
def get_predict(code):
    """获取预测数据"""
    try:
        predictor = StockPredictor(code)
        result = predictor.predict()

        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/predict/report/<code>", methods=["GET"])
def get_predict_report(code):
    """获取预测报告（文本）"""
    try:
        predictor = StockPredictor(code)
        report = predictor.generate_report()

        return jsonify({"success": True, "data": {"report": report}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/stocks", methods=["GET"])
def get_stocks():
    """获取股票配置列表"""
    config = config_loader.load_stocks_config()
    stocks = config.get("stocks", []) if config else []
    return jsonify({"success": True, "data": stocks})


@api.route("/stocks", methods=["POST"])
def add_stock():
    """添加股票"""
    try:
        data = request.get_json()
        code = data.get("code", "").strip()
        name = data.get("name", "").strip()
        market = data.get("market", "sz").strip()
        alias = data.get("alias", "").strip()
        notes = data.get("notes", "").strip()

        if not code or not name:
            return jsonify({"success": False, "error": "股票代码和名称不能为空"}), 400

        config = config_loader.load_stocks_config()
        if not config:
            config = {"stocks": [], "settings": {}}

        # 检查是否已存在
        for stock in config.get("stocks", []):
            if stock["code"] == code:
                return jsonify({"success": False, "error": f"股票 {code} 已存在"}), 400

        # 添加新股票
        new_stock = {
            "code": code,
            "name": name,
            "market": market,
            "enabled": True,
            "alias": alias or name,
            "notes": notes,
        }
        config["stocks"].append(new_stock)
        config["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        config["version"] = config.get("version", 1) + 1

        if not config_loader.save_config("stocks_config.json", config):
            return jsonify({"success": False, "error": "保存配置失败"}), 500

        return jsonify(
            {"success": True, "data": new_stock, "message": f"已添加股票 {name}({code})"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/stocks/<code>", methods=["DELETE"])
def delete_stock(code):
    """删除股票"""
    try:
        config = config_loader.load_stocks_config()
        if not config:
            return jsonify({"success": False, "error": f"股票 {code} 不存在"}), 404

        # 查找并删除
        found = False
        new_stocks = []
        for stock in config.get("stocks", []):
            if stock["code"] == code:
                found = True
            else:
                new_stocks.append(stock)

        if not found:
            return jsonify({"success": False, "error": f"股票 {code} 不存在"}), 404

        config["stocks"] = new_stocks
        config["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        config["version"] = config.get("version", 1) + 1

        if not config_loader.save_config("stocks_config.json", config):
            return jsonify({"success": False, "error": "保存配置失败"}), 500

        return jsonify({"success": True, "message": f"已删除股票 {code}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@api.route("/stocks/<code>/toggle", methods=["POST"])
def toggle_stock(code):
    """切换股票启用状态"""
    try:
        config = config_loader.load_stocks_config()
        if not config:
            return jsonify({"success": False, "error": f"股票 {code} 不存在"}), 404

        found = False
        for stock in config.get("stocks", []):
            if stock["code"] == code:
                found = True
                stock["enabled"] = not stock.get("enabled", True)
                new_status = stock["enabled"]
                break

        if not found:
            return jsonify({"success": False, "error": f"股票 {code} 不存在"}), 404

        config["updated_at"] = datetime.now().strftime("%Y-%m-%d")
        config["version"] = config.get("version", 1) + 1

        if not config_loader.save_config("stocks_config.json", config):
            return jsonify({"success": False, "error": "保存配置失败"}), 500

        return jsonify(
            {
                "success": True,
                "data": {"enabled": new_status},
                "message": f"股票 {code} 已{'启用' if new_status else '禁用'}",
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
