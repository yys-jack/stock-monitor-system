# 🚀 快速开始指南

## 5 分钟上手

### 1️⃣ 克隆项目

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
```

### 2️⃣ 安装依赖

```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 Make（推荐）
make install
```

### 3️⃣ 配置飞书推送

```bash
# 复制配置模板
cp config/feishu_config.example.json config/feishu_config.json

# 编辑配置，填写你的飞书应用凭证
vim config/feishu_config.json
```

**获取飞书凭证：**
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `app_id` 和 `app_secret`
4. 在应用中添加用户 ID

### 4️⃣ 配置股票

编辑 `config/stocks_config.json`：

```json
{
  "stocks": [
    {
      "code": "000063",
      "name": "中兴通讯",
      "market": "sz",
      "enabled": true,
      "alias": "ZTE"
    }
  ],
  "settings": {
    "push_interval_minutes": 30,
    "alert_threshold_up": 5.0,
    "alert_threshold_down": -5.0
  }
}
```

### 5️⃣ 启动服务

#### Web 界面（推荐）
```bash
python app.py
# 访问 http://localhost:5000
```

#### 手动运行监控
```bash
# 股票监控
python scripts/multi_stocks_monitor.py

# 黄金监控
python scripts/gold_monitor.py

# 预测推送
python scripts/prediction_push.py
```

### 6️⃣ 设置定时任务（可选）

```bash
# 自动安装 cron 任务
bash cron_install.sh
```

---

## 📋 常用命令

```bash
# 开发环境安装
make dev

# 运行测试
make test

# 代码检查
make lint

# 清理缓存
make clean

# 启动 Web 界面
make run-web

# 运行监控脚本
make run-monitor
make run-gold
```

---

## 🐳 Docker 部署

```bash
# 构建镜像
docker build -t stock-monitor-system .

# 运行容器
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  stock-monitor-system
```

---

## ❓ 常见问题

### Q: 飞书推送不工作？
A: 检查 `config/feishu_config.json` 中的凭证是否正确，确保飞书应用已启用。

### Q: 股价数据获取失败？
A: 检查网络连接，腾讯财经 API 可能需要稳定的网络环境。

### Q: 如何添加更多股票？
A: 在 `config/stocks_config.json` 的 `stocks` 数组中添加新的股票配置。

### Q: 定时任务不执行？
A: 检查 cron 服务状态：`systemctl status cron`，查看日志：`tail -f /var/log/cron`

---

## 📚 更多文档

- [技术栈说明](TECH_STACK.md)
- [敏捷开发流程](AGILE_DEVELOPMENT.md)
- [Git 工作流](GIT_WORKFLOW.md)
- [测试指南](TESTING.md)
- [版本路线图](ROADMAP.md)

---

_遇到问题？查看 [README.md](README.md) 或提 Issue。_
