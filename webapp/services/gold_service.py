#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金价格服务层
"""

from typing import Optional, Dict, Any
import akshare as ak


class GoldService:
    """黄金价格服务类"""
    
    def fetch_gold_price(self) -> Optional[Dict[str, Any]]:
        """
        获取黄金价格（国内 + 国际）
        
        数据源说明:
        - 国内金价：上期所黄金期货 AU2606 主力合约（实时）
        - 国际金价：伦敦金 (XAU) + COMEX 黄金期货
        
        注意：期货价格通常比现货高 3-5 元/克（升水），这是正常现象。
        """
        gold_data = {}
        
        try:
            # 获取上期所黄金期货实时行情
            df = ak.futures_zh_realtime(symbol="黄金")
            
            if len(df) > 0:
                # 使用 AU2606 主力合约（最近月份）
                main_contract = df[df['symbol'] == 'AU2606']
                if len(main_contract) == 0:
                    main_contract = df[df['symbol'] == 'AU0']
                if len(main_contract) == 0:
                    main_contract = df.iloc[0:1]
                
                row = main_contract.iloc[0]
                current_cny_g = float(row.get('trade', 0))
                prev_settlement = float(row.get('prevsettlement', current_cny_g))
                change_pct = float(row.get('changepercent', 0))
                change_cny_g = current_cny_g - prev_settlement
                
                # 估算国际金价（反向换算）
                exchange_rate = 7.2
                current_usd_oz = (current_cny_g * 31.1035) / exchange_rate
                
                # 期货升水校正（减去升水得到近似现货价）
                futures_premium = 3.5
                spot_cny_g = current_cny_g - futures_premium
                
                gold_data = {
                    "source": "SHFE",
                    "symbol": row.get('symbol', 'AU2606'),
                    "current_cny_g": current_cny_g,  # 期货价格
                    "spot_cny_g": spot_cny_g,  # 估算现货价
                    "current_usd_oz": current_usd_oz,
                    "change_cny_g": change_cny_g,
                    "change_pct": change_pct,
                    "update_time": row.get('tradetime', ''),
                }
            else:
                return None
                
        except Exception as e:
            print(f"[ERROR] 获取黄金价格失败：{e}")
            return None
        
        return gold_data
    
    def format_price_message(self, gold_data: Dict[str, Any]) -> str:
        """格式化黄金价格消息"""
        change_symbol = "📈" if gold_data['change_pct'] > 0 else "📉" if gold_data['change_pct'] < 0 else "➡️"
        
        return f"""{change_symbol}【{gold_data.get('symbol', '黄金')} 实时金价】
⏰ 时间：{gold_data.get('update_time', '')}

💹 国内金价（上期所期货）
  期货价：{gold_data['current_cny_g']:.2f} 元/克
  现货价：{gold_data['spot_cny_g']:.2f} 元/克（估算）
  涨跌额：{gold_data['change_cny_g']:+.2f} 元/克
  涨跌幅：{gold_data['change_pct']:+.2f}%

🌍 国际金价（估算）
  {gold_data['current_usd_oz']:.2f} 美元/盎司

📊 说明
  数据来源：上海期货交易所
  期货升水：约 3-5 元/克（正常现象）
  现货价 = 期货价 - 升水估算"""


# 全局实例
gold_service = GoldService()
