#!/usr/bin/env python3
"""
股票预测定时推送脚本
专用于 cron 任务调用，执行技术分析和预测推送

用法:
    python3 scripts/cron_prediction_push.py
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.prediction_push import main as push_predictions


if __name__ == "__main__":
    print("=" * 60)
    print("🔮 股票预测定时推送任务")
    print("=" * 60)
    
    success = push_predictions()
    
    if success:
        print("\n✅ 预测推送任务执行成功")
        sys.exit(0)
    else:
        print("\n❌ 预测推送任务执行失败")
        sys.exit(1)
