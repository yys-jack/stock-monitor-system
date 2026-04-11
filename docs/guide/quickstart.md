# 快速开始

> 5 分钟上手股票监控系统

## 前置要求

- Python 3.8+
- pip 包管理器
- 飞书应用（可选，用于推送通知）

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
# 或使用 Make
make install
```

### 4. 配置飞书推送（可选）

```bash
cp config/feishu_config.example.json config/feishu_config.json
vim config/feishu_config.json
```

**获取飞书凭证：**
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `app_id` 和 `app_secret`
4. 在应用中添加用户 ID

> ⚠️ **注意：** `feishu_config.json` 已加入 `.gitignore`，不会被提交到 Git。

### 5. 配置股票

```bash
cp config/stocks_config.example.json config/stocks_config.json
vim config/stocks_config.json
```

示例配置：
```json
{
  "stocks": [
    {
      "code": "000063",
      "name": "中兴通讯",
      "market": "sz",
      "enabled": true,
      "alias": "ZTE",
      "notes": "5G 通信设备龙头"
    }
  ]
}
```

### 6. 启动服务

#### Web 界面（推荐）
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：http://localhost:8000

#### 命令行监控
```bash
python3 scripts/multi_stocks_monitor.py
```

## 下一步

- [配置说明](config.md) - 详细配置选项
- [部署指南](deployment.md) - 生产环境部署
- [故障排除](troubleshooting.md) - 常见问题
