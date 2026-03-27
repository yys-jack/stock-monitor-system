#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证历史预测准确性
用途：获取实际股价，与前一天预测对比，更新历史记录
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional

# 配置
PROJECT_ROOT = Path(__file__).parent.parent
HISTORY_FILE = PROJECT_ROOT / "data" / "prediction_history.json"

def load_prediction_history() -> Dict:
    """加载预测历史记录"""
    if not HISTORY_FILE.exists():
        return {"version": 1, "predictions": []}
    
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_prediction_history(history: Dict):
    """保存预测历史记录"""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_stock_price(code: str) -> Optional[Dict]:
    """从腾讯财经获取股票价格"""
    try:
        market = 'sh' if code.startswith('6') else 'sz'
        url = f"https://qt.gtimg.cn/q={market}{code}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "gbk"
        
        if resp.status_code != 200:
            return None
        
        content = resp.text.strip()
        if not content.startswith("v_"):
            return None
        
        data_str = content.split("=\"")[1].rstrip("\";")
        fields = data_str.split("~")
        
        if len(fields) < 35:
            return None
        
        return {
            "name": fields[1],
            "code": fields[2],
            "current": float(fields[3]) if fields[3] else 0,
            "prev_close": float(fields[4]) if fields[4] else 0,
            "change_pct": float(fields[32]) if fields[32] else 0,
        }
    except Exception as e:
        print(f"[ERROR] 获取股价失败：{e}")
        return None

def verify_predictions():
    """验证历史预测"""
    print("🔍 验证历史预测准确性")
    print("="*60)
    
    history = load_prediction_history()
    predictions = history.get('predictions', [])
    
    # 找出需要验证的预测（未验证且是昨天的）
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    to_verify = [
        p for p in predictions
        if not p.get('verified') and p.get('predicted_at', '').startswith(yesterday)
    ]
    
    if not to_verify:
        print(f"[INFO] 没有需要验证的预测")
        print(f"[INFO] 历史预测总数：{len(predictions)}")
        return
    
    print(f"[INFO] 待验证预测数：{len(to_verify)}")
    print()
    
    verified_count = 0
    correct_count = 0
    
    for pred in to_verify:
        stock_code = pred.get('stock_code', '')
        if not stock_code:
            continue
        
        print(f"[INFO] 验证 {stock_code}...")
        
        # 获取当前股价
        price_data = get_stock_price(stock_code)
        if not price_data:
            print(f"  ❌ 获取股价失败")
            continue
        
        current_price = price_data['current']
        change_pct = price_data['change_pct']
        
        # 判断实际趋势
        if change_pct > 0.5:
            actual_trend = "上涨"
        elif change_pct < -0.5:
            actual_trend = "下跌"
        else:
            actual_trend = "震荡"
        
        # 对比预测
        predicted_trend = pred.get('predicted_trend', '')
        is_correct = (predicted_trend == actual_trend) or (
            abs(change_pct) < 1 and predicted_trend in ["震荡", "观望"]
        )
        
        if is_correct:
            correct_count += 1
            status = "✅ 正确"
        else:
            status = "❌ 错误"
        
        print(f"  预测：{predicted_trend}")
        print(f"  实际：{actual_trend} ({change_pct:+.2f}%)")
        print(f"  结果：{status}")
        print()
        
        # 更新预测记录
        pred['actual_trend'] = actual_trend
        pred['actual_change_pct'] = change_pct
        pred['actual_price'] = current_price
        pred['verified'] = True
        pred['verified_at'] = datetime.now().isoformat()
        pred['is_correct'] = is_correct
        
        verified_count += 1
    
    # 保存更新后的历史记录
    save_prediction_history(history)
    
    # 统计准确率
    print("="*60)
    print(f"📊 验证结果汇总")
    print(f"  本次验证：{verified_count} 条")
    print(f"  正确：{correct_count} 条")
    print(f"  准确率：{correct_count/verified_count*100:.1f}%" if verified_count else "  准确率：N/A")
    
    # 计算总体准确率
    all_verified = [p for p in predictions if p.get('verified')]
    all_correct = [p for p in all_verified if p.get('is_correct')]
    
    if all_verified:
        overall_accuracy = len(all_correct) / len(all_verified) * 100
        print(f"\n📈 历史总体准确率：{overall_accuracy:.1f}% ({len(all_correct)}/{len(all_verified)})")
    
    print(f"\n[INFO] 历史记录已更新：{HISTORY_FILE}")

if __name__ == "__main__":
    verify_predictions()
