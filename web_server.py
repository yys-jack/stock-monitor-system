#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控系统 Web 界面
Flask 后端服务器
"""

from flask import Flask, render_template, jsonify
import akshare as ak
import requests
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# 配置
DEFAULT_STOCK = "000063"
STOCKS_CONFIG = Path(__file__).parent / "stocks_config.json"

def load_stocks():
    """加载股票配置"""
    if STOCKS_CONFIG.exists():
        with open(STOCKS_CONFIG, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('stocks', [])
    return [{"code": DEFAULT_STOCK, "name": "中兴通讯", "market": "sz"}]

def fetch_stock_price(code, market):
    """获取实时股价"""
    try:
        url = f"https://qt.gtimg.cn/q={market}{code}"
        resp = requests.get(url, timeout=10)
        resp.encoding = "gbk"
        
        if resp.status_code == 200:
            content = resp.text.strip()
            if content.startswith("v_"):
                fields = content.split("=\"")[1].rstrip("\";").split("~")
                if len(fields) >= 35:
                    return {
                        "name": fields[1],
                        "code": fields[2],
                        "current": float(fields[3]) if fields[3] else 0,
                        "prev_close": float(fields[4]) if fields[4] else 0,
                        "change_pct": float(fields[32]) if fields[32] else 0,
                        "volume": int(fields[6]) if fields[6] else 0,
                        "high": float(fields[33]) if fields[33] else 0,
                        "low": float(fields[34]) if fields[34] else 0,
                    }
    except Exception as e:
        print(f"Error fetching price: {e}")
    return None

def fetch_news(code):
    """获取新闻"""
    try:
        news_df = ak.stock_news_em(symbol=code)
        if len(news_df) > 0:
            news_list = []
            for idx, row in news_df.head(10).iterrows():
                news_list.append({
                    "title": row.get('新闻标题', '')[:80],
                    "source": row.get('文章来源', '东方财富'),
                    "date": str(row.get('发布时间', ''))[:16],
                    "url": row.get('新闻链接', ''),
                })
            return news_list
    except Exception as e:
        print(f"Error fetching news: {e}")
    return []

def fetch_history(code):
    """获取历史行情"""
    try:
        from akshare import stock_zh_a_hist
        df = stock_zh_a_hist(symbol=code, period="daily", start_date="20260201")
        if len(df) > 0:
            history = []
            for idx, row in df.tail(30).iterrows():
                history.append({
                    "date": str(row.get('日期', '')),
                    "close": float(row.get('收盘', 0)),
                    "change": float(row.get('涨跌幅', 0)),
                })
            return history
    except Exception as e:
        print(f"Error fetching history: {e}")
    return []

@app.route('/')
def index():
    """首页"""
    stocks = load_stocks()
    return render_template('index.html', stocks=stocks, default_stock=DEFAULT_STOCK)

@app.route('/api/stock/<code>')
def api_stock(code):
    """获取股票实时数据"""
    stocks = load_stocks()
    stock_info = next((s for s in stocks if s['code'] == code), None)
    
    if not stock_info:
        stock_info = {"code": code, "name": "Unknown", "market": "sz"}
    
    price_data = fetch_stock_price(code, stock_info.get('market', 'sz'))
    
    if price_data:
        return jsonify({
            "success": True,
            "data": {
                "stock": stock_info,
                "price": price_data,
                "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
        })
    else:
        return jsonify({
            "success": False,
            "error": "Failed to fetch stock price"
        }), 500

@app.route('/api/news/<code>')
def api_news(code):
    """获取新闻"""
    news_list = fetch_news(code)
    return jsonify({
        "success": True,
        "data": news_list
    })

@app.route('/api/history/<code>')
def api_history(code):
    """获取历史行情"""
    history = fetch_history(code)
    return jsonify({
        "success": True,
        "data": history
    })

@app.route('/api/overview')
def api_overview():
    """获取概览数据"""
    stocks = load_stocks()
    overview = []
    
    for stock in stocks:
        if stock.get('enabled', True):
            price_data = fetch_stock_price(stock['code'], stock.get('market', 'sz'))
            if price_data:
                overview.append({
                    "code": stock['code'],
                    "name": stock['name'],
                    "alias": stock.get('alias', ''),
                    "current": price_data['current'],
                    "change_pct": price_data['change_pct'],
                })
    
    return jsonify({
        "success": True,
        "data": overview
    })

@app.route('/api/predict/<code>')
def api_predict(code):
    """获取预测数据"""
    try:
        from stock_predictor import StockPredictor
        
        predictor = StockPredictor(code)
        signal = predictor.predict()
        
        return jsonify({
            "success": True,
            "data": signal
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/predict/report/<code>')
def api_predict_report(code):
    """获取预测报告（文本）"""
    try:
        from stock_predictor import StockPredictor
        
        predictor = StockPredictor(code)
        report = predictor.generate_report()
        
        return jsonify({
            "success": True,
            "data": {"report": report}
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stocks', methods=['GET'])
def api_get_stocks():
    """获取股票配置列表"""
    stocks = load_stocks()
    return jsonify({
        "success": True,
        "data": stocks
    })

@app.route('/api/stocks', methods=['POST'])
def api_add_stock():
    """添加股票"""
    try:
        from flask import request
        
        data = request.get_json()
        code = data.get('code', '').strip()
        name = data.get('name', '').strip()
        market = data.get('market', 'sz').strip()
        alias = data.get('alias', '').strip()
        notes = data.get('notes', '').strip()
        
        if not code or not name:
            return jsonify({
                "success": False,
                "error": "股票代码和名称不能为空"
            }), 400
        
        # 加载现有配置
        if STOCKS_CONFIG.exists():
            with open(STOCKS_CONFIG, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {"version": 1, "updated_at": datetime.now().strftime('%Y-%m-%d'), "stocks": [], "settings": {}}
        
        # 检查是否已存在
        for stock in config.get('stocks', []):
            if stock['code'] == code:
                return jsonify({
                    "success": False,
                    "error": f"股票 {code} 已存在"
                }), 400
        
        # 添加新股票
        new_stock = {
            "code": code,
            "name": name,
            "market": market,
            "enabled": True,
            "alias": alias or name,
            "notes": notes
        }
        config['stocks'].append(new_stock)
        config['updated_at'] = datetime.now().strftime('%Y-%m-%d')
        config['version'] = config.get('version', 1) + 1
        
        # 保存配置
        with open(STOCKS_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True,
            "data": new_stock,
            "message": f"已添加股票 {name}({code})"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stocks/<code>', methods=['DELETE'])
def api_delete_stock(code):
    """删除股票"""
    try:
        if not STOCKS_CONFIG.exists():
            return jsonify({
                "success": False,
                "error": "配置文件不存在"
            }), 404
        
        with open(STOCKS_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 查找并删除
        found = False
        new_stocks = []
        for stock in config.get('stocks', []):
            if stock['code'] == code:
                found = True
            else:
                new_stocks.append(stock)
        
        if not found:
            return jsonify({
                "success": False,
                "error": f"股票 {code} 不存在"
            }), 404
        
        config['stocks'] = new_stocks
        config['updated_at'] = datetime.now().strftime('%Y-%m-%d')
        config['version'] = config.get('version', 1) + 1
        
        with open(STOCKS_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True,
            "message": f"已删除股票 {code}"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stocks/<code>/toggle', methods=['POST'])
def api_toggle_stock(code):
    """切换股票启用状态"""
    try:
        from flask import request
        
        if not STOCKS_CONFIG.exists():
            return jsonify({
                "success": False,
                "error": "配置文件不存在"
            }), 404
        
        with open(STOCKS_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        found = False
        for stock in config.get('stocks', []):
            if stock['code'] == code:
                found = True
                stock['enabled'] = not stock.get('enabled', True)
                new_status = stock['enabled']
                break
        
        if not found:
            return jsonify({
                "success": False,
                "error": f"股票 {code} 不存在"
            }), 404
        
        config['updated_at'] = datetime.now().strftime('%Y-%m-%d')
        config['version'] = config.get('version', 1) + 1
        
        with open(STOCKS_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            "success": True,
            "data": {"enabled": new_status},
            "message": f"股票 {code} 已{'启用' if new_status else '禁用'}"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🦞 股票监控系统 Web 界面启动")
    print("="*60)
    print("访问地址：http://localhost:5000")
    print("="*60)
    app.run(host='0.0.0.0', port=5000, debug=True)
