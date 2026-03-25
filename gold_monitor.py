#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金价格监控脚本
监控国内黄金现货价格（AU9999）和国际黄金期货价格
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional

# 配置
CONFIG_FILE = Path(__file__).parent / "gold_config.json"
FEISHU_CONFIG_FILE = Path(__file__).parent / "feishu_config.json"
OUTPUT_DIR = Path(__file__).parent / "output"

def load_feishu_config() -> dict:
    """加载飞书配置文件"""
    if not FEISHU_CONFIG_FILE.exists():
        return {"enabled": False, "user_id": "", "app_id": "", "app_secret": "", "retry_times": 3, "retry_delay": 2}
    
    with open(FEISHU_CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
        return config.get('feishu', {})

FEISHU_CONFIG = load_feishu_config()

def load_gold_config() -> dict:
    """加载黄金配置文件"""
    if not CONFIG_FILE.exists():
        print(f"[ERROR] 配置文件不存在：{CONFIG_FILE}")
        return None
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_gold_price() -> Optional[dict]:
    """
    获取黄金价格（实时国内金价）
    
    数据源说明:
    - 国内金价：上海期货交易所黄金期货主力合约（实时）
    - 备用：COMEX 黄金期货（腾讯财经接口，国际参考）
    
    上期所黄金期货 (AU0/AU2606 等) 是实时交易的国内黄金价格，准确性高。
    """
    # 方案 1: 获取上期所黄金期货实时行情（推荐）
    try:
        import akshare as ak
        # 获取黄金期货实时行情
        df = ak.futures_zh_realtime(symbol="黄金")
        
        if len(df) > 0:
            # 优先使用黄金连续合约 (AU0) 或主力合约
            main_contract = df[df['symbol'] == 'AU0']
            if len(main_contract) == 0:
                main_contract = df.iloc[0:1]  # 使用第一行（通常是主力）
            
            row = main_contract.iloc[0]
            current_cny_g = float(row.get('trade', 0))
            prev_settlement = float(row.get('prevsettlement', current_cny_g))
            change_pct = float(row.get('changepercent', 0))
            change_cny_g = current_cny_g - prev_settlement
            
            # 估算国际金价（反向换算）
            exchange_rate = 7.2
            current_usd_oz = (current_cny_g * 31.1035) / exchange_rate
            
            return {
                "name": "上期所黄金期货",
                "code": "AU0",
                "current_cny_g": current_cny_g,
                "current_usd_oz": current_usd_oz,
                "prev_close_cny_g": prev_settlement,
                "prev_close_usd_oz": (prev_settlement * 31.1035) / exchange_rate,
                "change_cny_g": change_cny_g,
                "change_usd_oz": change_cny_g * 31.1035 / exchange_rate,
                "change_pct": change_pct,
                "high_usd_oz": float(row.get('high', current_usd_oz * 1.01)),
                "low_usd_oz": float(row.get('low', current_usd_oz * 0.99)),
                "source": "SHFE",
            }
    except Exception as e:
        print(f"[WARN] 获取上期所金价失败：{e}")
    
    # 方案 2: 降级使用 COMEX 国际金价（腾讯财经）
    try:
        url = "https://qt.gtimg.cn/q=hf_GC"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "gbk"
        
        if resp.status_code != 200:
            return None
        
        content = resp.text.strip()
        if not content.startswith("v_hf_GC="):
            print(f"[WARN] 响应格式异常：{content[:50]}")
            return None
        
        # 解析：v_hf_GC="4620.30,4.20,4618.80,4619.20,4633.40,4491.70,..."
        data_str = content.split('="')[1].rstrip('";')
        fields = data_str.split(",")
        
        if len(fields) < 6:
            print(f"[WARN] 字段数量不足：{len(fields)}")
            return None
        
        # 解析字段：当前价，涨跌，买价，卖价，最高，最低
        current_usd_oz = float(fields[0]) if fields[0] else 0
        change_usd = float(fields[1]) if fields[1] else 0
        high_usd_oz = float(fields[4]) if fields[4] else 0
        low_usd_oz = float(fields[5]) if fields[5] else 0
        
        # 转换为人民币/克（1 盎司≈31.1035 克，汇率≈7.2）
        exchange_rate = 7.2
        current_cny_g = (current_usd_oz * exchange_rate) / 31.1035
        prev_close_usd = current_usd_oz - change_usd
        prev_cny_g = (prev_close_usd * exchange_rate) / 31.1035
        change_cny_g = current_cny_g - prev_cny_g
        change_pct = (change_usd / prev_close_usd) * 100 if prev_close_usd else 0
        
        return {
            "name": "COMEX 黄金期货",
            "code": "GC",
            "current_usd_oz": current_usd_oz,
            "current_cny_g": current_cny_g,
            "prev_close_usd_oz": prev_close_usd,
            "prev_close_cny_g": prev_cny_g,
            "change_usd_oz": change_usd,
            "change_cny_g": change_cny_g,
            "change_pct": change_pct,
            "high_usd_oz": high_usd_oz,
            "low_usd_oz": low_usd_oz,
            "source": "COMEX",
        }
    except Exception as e:
        print(f"[ERROR] 获取黄金价格失败：{e}")
        import traceback
        traceback.print_exc()
        return None

def format_gold_message(gold_data: dict, config: dict) -> str:
    """格式化黄金价格消息"""
    current_cny = gold_data.get("current_cny_g", 0)
    current_usd = gold_data.get("current_usd_oz", 0)
    change_pct = gold_data.get("change_pct", 0)
    change_cny = gold_data.get("change_cny_g", 0)
    
    change_symbol = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➡️"
    
    alias = config.get("alias", "黄金")
    notes = config.get("notes", "")
    
    return f"""{change_symbol}【{gold_data['name']}】黄金价格提醒
🏷️ 别名：{alias}
⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

💹 实时金价
  折合人民币：{current_cny:.2f} 元/克
  国际金价：{current_usd:.2f} 美元/盎司
  涨跌额：{change_cny:+.2f} 元/克
  涨跌幅：{change_pct:+.2f}%
  
📊 今日行情
  昨收：{gold_data.get('prev_close_usd_oz', 0):.2f} 美元/盎司
  最高：{gold_data.get('high_usd_oz', 0):.2f} 美元/盎司
  最低：{gold_data.get('low_usd_oz', 0):.2f} 美元/盎司

---
🤖 黄金监控系统 | {notes}"""

def send_feishu_message(message: str, retry_times: int = None) -> bool:
    """发送飞书消息（带重试机制）"""
    if not FEISHU_CONFIG.get("enabled"):
        print("[INFO] 飞书推送未启用")
        return False
    
    if retry_times is None:
        retry_times = FEISHU_CONFIG.get("retry_times", 3)
    
    retry_delay = FEISHU_CONFIG.get("retry_delay", 2)
    
    for attempt in range(1, retry_times + 1):
        try:
            if attempt > 1:
                print(f"[INFO] 重试推送 (第 {attempt}/{retry_times} 次)...")
                import time
                time.sleep(retry_delay)
            
            # 1. 获取 tenant_access_token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": FEISHU_CONFIG["app_id"],
                "app_secret": FEISHU_CONFIG["app_secret"]
            }
            token_resp = requests.post(token_url, json=token_data, timeout=10)
            if token_resp.status_code != 200:
                continue
            
            token_result = token_resp.json()
            if token_result.get("code") != 0:
                continue
            
            tenant_token = token_result.get("tenant_access_token")
            
            # 2. 发送消息
            msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
            headers = {
                "Authorization": f"Bearer {tenant_token}",
                "Content-Type": "application/json"
            }
            msg_data = {
                "receive_id": FEISHU_CONFIG["user_id"],
                "msg_type": "text",
                "content": json.dumps({"text": message})
            }
            
            msg_resp = requests.post(msg_url, headers=headers, json=msg_data, timeout=10)
            if msg_resp.status_code == 200:
                result = msg_resp.json()
                if result.get("code") == 0:
                    print(f"[INFO] ✅ 飞书推送成功！")
                    return True
            
        except Exception as e:
            print(f"[ERROR] 飞书推送异常 (第 {attempt} 次): {e}")
        
        if attempt < retry_times:
            print(f"[INFO] 等待 {retry_delay} 秒后重试...")
    
    print(f"[ERROR] ❌ 飞书推送失败，已重试 {retry_times} 次")
    return False

def main():
    """主函数"""
    print(f"🥇 黄金监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 加载配置
    config = load_gold_config()
    if not config:
        return False
    
    settings = config.get("settings", {})
    
    print(f"[INFO] 监控类型：{config.get('type', 'COMEX')}")
    
    # 获取黄金价格
    print(f"\n[INFO] 获取黄金价格...")
    
    gold_data = fetch_gold_price()
    
    if not gold_data:
        print("[ERROR] 黄金价格获取失败")
        return False
    
    source = gold_data.get('source', 'Unknown')
    print(f"  ✅ 当前价：{gold_data['current_cny_g']:.2f} 元/克 ({gold_data['current_usd_oz']:.2f} 美元/盎司)")
    print(f"  📍 数据源：{source}")
    
    if source == "COMEX":
        print(f"  ⚠️  注意：COMEX 换算价可能与国内实际金价存在差异")
    
    # 格式化消息
    message = format_gold_message(gold_data, config)
    
    # 写入文件
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "gold_price.txt"
    output_file.write_text(message, encoding="utf-8")
    print(f"[INFO] 消息已写入：{output_file}")
    
    # 飞书推送
    if FEISHU_CONFIG.get("enabled"):
        print(f"[INFO] 发送飞书消息...")
        send_feishu_message(message)
    
    print(f"\n✅ 黄金监控完成！")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
