# 🚀 快速开始

## 5 分钟上手

### 1. 克隆项目

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
# 或 make install
```

### 3. 配置

```bash
# 飞书配置
cp config/feishu_config.example.json config/feishu_config.json
vim config/feishu_config.json

# 股票配置
cp config/stocks_config.example.json config/stocks_config.json
vim config/stocks_config.json
```

**获取飞书凭证：** 访问 [飞书开放平台](https://open.feishu.cn/) 创建应用。

### 4. 启动

```bash
# Web 界面
python app.py
# 访问 http://localhost:5000

# 手动运行监控
python scripts/multi_stocks_monitor.py
```

### 5. 定时任务（可选）

```bash
bash cron_install.sh install
```

---

## 常用命令

```bash
make install      # 安装依赖
make test         # 运行测试
make lint         # 代码检查
make run-web      # 启动 Web
make clean        # 清理缓存
```

---

## 🐳 Docker 部署

```bash
docker build -t stock-monitor-system .
docker run -d -p 5000:5000 \
  -v $(pwd)/config:/app/config \
  stock-monitor-system
```

---

**详细文档:** [DEPLOYMENT.md](DEPLOYMENT.md) | [CONTRIBUTING.md](CONTRIBUTING.md)
