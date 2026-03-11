#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票预测推送脚本
生成预测报告并推送到飞书
"""

import requests
import json
from datetime import datetime
from pathlib import Path
from stock_predictor import StockPredictor

# 配置
CONFIG = {
    "stock_code": "000063",
    "stock_name": "中兴通讯",
    
    # 飞书配置
    "feishu": {
        "enabled": True,
        "user_id": "ou_02e3153454246dd33432d6a00d3db941",
        "app_id": "cli_a927c1dca5b81cb6",
        "app_secret": "hqIwARj5n11Yy4WEeqVnic5GViL4zDTs",
        "retry_times": 3,
        "retry_delay": 2,
    },
    
    # 推送时间（每个交易日 15:30 推送，收盘后）
    "push_time": "15:30",
}

def generate_prediction_report(stock_code: str) -> dict:
    """生成预测报告"""
    try:
        predictor = StockPredictor(stock_code)
        
        # 获取数据
        df = predictor.fetch_history_data(days=60)
        if df.empty:
            return {"success": False, "error": "获取数据失败"}
        
        # 计算指标
        df = predictor.calculate_ma(df)
        df = predictor.calculate_macd(df)
        df = predictor.calculate_rsi(df)
        df = predictor.calculate_kdj(df)
        df = predictor.calculate_boll(df)
        
        # 趋势分析
        trend_analysis = predictor.analyze_trend(df)
        prediction = predictor.predict_price(df, days=5)
        
        # 获取最新数据
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        return {
            "success": True,
            "data": {
                "stock_code": stock_code,
                "stock_name": predictor.stock_name,
                "date": datetime.now().strftime('%Y-%m-%d'),
                "current_price": float(latest.get('收盘', 0)),
                "change_pct": float(latest.get('涨跌幅', 0)),
                "volume": int(latest.get('成交量', 0)),
                
                # 技术指标
                "ma5": float(latest.get('MA5', 0)),
                "ma10": float(latest.get('MA10', 0)),
                "ma20": float(latest.get('MA20', 0)),
                "macd": float(latest.get('MACD', 0)),
                "rsi": float(latest.get('RSI', 0)),
                "kdj_k": float(latest.get('K', 0)),
                "kdj_d": float(latest.get('D', 0)),
                
                # 预测结果
                "signal": trend_analysis.get('overall_signal', '中性'),
                "trend": trend_analysis.get('trend', '震荡'),
                "confidence": prediction.get('confidence', 0),
                "predicted_change": prediction.get('change_pct', 0),
                "support_level": prediction.get('support', 0),
                "pressure_level": prediction.get('pressure', 0),
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def format_prediction_message(report: dict) -> str:
    """格式化预测消息"""
    data = report['data']
    
    # 信号图标
    signal = data['signal']
    if signal == '买入':
        signal_icon = '🟢'
    elif signal == '卖出':
        signal_icon = '🔴'
    else:
        signal_icon = '🟡'
    
    # 置信度
    confidence = data['confidence']
    if confidence > 70:
        confidence_level = '高'
    elif confidence > 50:
        confidence_level = '中'
    else:
        confidence_level = '低'
    
    message = f"""{signal_icon}【{data['stock_name']} 预测报告】
📅 日期：{data['date']}

💹 当前股价
  收盘价：¥{data['current_price']:.2f}
  涨跌幅：{data['change_pct']:+.2f}%
  成交量：{data['volume']/10000:.1f}万手

📊 技术指标
  MA5:  ¥{data['ma5']:.2f}  | MA10: ¥{data['ma10']:.2f}
  MA20: ¥{data['ma20']:.2f}
  MACD: {data['macd']:.2f}  | RSI: {data['rsi']:.1f}
  KDJ:  K={data['kdj_k']:.1f} D={data['kdj_d']:.1f}

🔮 趋势预测
  信号：{signal_icon} {signal}
  趋势：{data['trend']}
  置信度：{confidence_level} ({confidence:.1f}%)
  预计涨跌：{data['predicted_change']:+.2f}%
  
📈 关键价位
  支撑位：¥{data['support_level']:.2f}
  压力位：¥{data['pressure_level']:.2f}

---
🤖 AI 预测 | 仅供参考，不构成投资建议"""

    return message

def send_feishu_message(message: str) -> bool:
    """发送飞书消息"""
    config = CONFIG['feishu']
    
    if not config.get('enabled'):
        print("[INFO] 飞书推送未启用")
        return False
    
    retry_times = config.get('retry_times', 3)
    retry_delay = config.get('retry_delay', 2)
    
    for attempt in range(1, retry_times + 1):
        try:
            if attempt > 1:
                print(f"[INFO] 重试推送 (第 {attempt}/{retry_times} 次)...")
                import time
                time.sleep(retry_delay)
            
            # 获取 token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": config["app_id"],
                "app_secret": config["app_secret"]
            }
            token_resp = requests.post(token_url, json=token_data, timeout=10)
            if token_resp.status_code != 200:
                continue
            
            token_result = token_resp.json()
            if token_result.get("code") != 0:
                continue
            
            tenant_token = token_result.get("tenant_access_token")
            
            # 发送消息
            msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
            headers = {
                "Authorization": f"Bearer {tenant_token}",
                "Content-Type": "application/json"
            }
            msg_data = {
                "receive_id": config["user_id"],
                "msg_type": "text",
                "content": json.dumps({"text": message})
            }
            
            msg_resp = requests.post(msg_url, headers=headers, json=msg_data, timeout=10)
            if msg_resp.status_code == 200:
                result = msg_resp.json()
                if result.get("code") == 0:
                    print(f"[INFO] ✅ 飞书推送成功！")
                    return True
            
            print(f"[WARN] 飞书发送失败：{msg_resp.json() if msg_resp.text else msg_resp.status_code}")
        
        except Exception as e:
            print(f"[ERROR] 飞书推送异常 (第 {attempt} 次): {e}")
        
        if attempt < retry_times:
            print(f"[INFO] 等待 {retry_delay} 秒后重试...")
    
    print(f"[ERROR] ❌ 飞书推送失败，已重试 {retry_times} 次")
    return False

def main():
    """主函数"""
    print(f"🔮 股票预测推送 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    stock_code = CONFIG['stock_code']
    print(f"[INFO] 生成 {stock_code} 预测报告...")
    
    report = generate_prediction_report(stock_code)
    
    if not report['success']:
        print(f"[ERROR] 生成预测失败：{report['error']}")
        return False
    
    data = report['data']
    print(f"[INFO] 当前股价：¥{data['current_price']:.2f} ({data['change_pct']:+.2f}%)")
    print(f"[INFO] 预测信号：{data['signal']} (置信度：{data['confidence']:.1f}%)")
    
    # 格式化消息
    message = format_prediction_message(report)
    
    # 写入文件
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"prediction_{stock_code}.txt"
    output_file.write_text(message, encoding='utf-8')
    print(f"[INFO] 报告已写入：{output_file}")
    
    # 发送飞书
    if CONFIG['feishu'].get('enabled'):
        print(f"[INFO] 发送飞书消息...")
        success = send_feishu_message(message)
        return success
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
