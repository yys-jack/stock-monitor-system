# 📦 部署指南

## 本地开发环境

### 1. 安装 Python

```bash
# macOS
brew install python@3.13

# Ubuntu/Debian
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip

# Windows
# 从 https://python.org 下载安装
```

### 2. 克隆项目

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
```

### 3. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
# 或
make install
```

### 5. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填写配置
```

### 6. 运行

```bash
# Web 界面
python app.py

# 或
make run-web
```

---

## 生产环境部署

### 方案 A: 直接部署

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置飞书和股票
vim config/feishu_config.json
vim config/stocks_config.json

# 3. 安装定时任务
bash cron_install.sh

# 4. 启动 Web 服务（使用 Gunicorn）
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 方案 B: Docker 部署

```bash
# 1. 构建镜像
docker build -t stock-monitor-system .

# 2. 运行容器
docker run -d \
  --name stock-monitor \
  -p 5000:5000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/data:/app/data \
  -e FEISHU_APP_ID=your_app_id \
  -e FEISHU_APP_SECRET=your_app_secret \
  stock-monitor-system

# 3. 查看日志
docker logs -f stock-monitor
```

### 方案 C: Docker Compose

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - FEISHU_APP_ID=${FEISHU_APP_ID}
      - FEISHU_APP_SECRET=${FEISHU_APP_SECRET}
    restart: unless-stopped

  monitor:
    build: .
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
    command: python scripts/multi_stocks_monitor.py
    environment:
      - FEISHU_APP_ID=${FEISHU_APP_ID}
      - FEISHU_APP_SECRET=${FEISHU_APP_SECRET}
    restart: unless-stopped
```

运行：

```bash
docker-compose up -d
```

---

## 云服务器部署

### 1. 准备服务器

```bash
# 推荐使用 Ubuntu 22.04+
# 确保已安装 Python 3.8+ 和 Git
```

### 2. 配置防火墙

```bash
# 开放 5000 端口
sudo ufw allow 5000/tcp
sudo ufw enable
```

### 3. 部署项目

```bash
# 克隆项目
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system

# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 配置
cp config/feishu_config.example.json config/feishu_config.json
vim config/feishu_config.json
```

### 4. 设置 Systemd 服务

创建 `/etc/systemd/system/stock-monitor.service`:

```ini
[Unit]
Description=Stock Monitor System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/stock-monitor-system
Environment="PATH=/path/to/stock-monitor-system/venv/bin"
ExecStart=/path/to/stock-monitor-system/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable stock-monitor
sudo systemctl start stock-monitor
sudo systemctl status stock-monitor
```

### 5. 配置 Nginx 反向代理

创建 `/etc/nginx/sites-available/stock-monitor`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/stock-monitor /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 监控和维护

### 查看日志

```bash
# 应用日志
tail -f logs/*.log

# Systemd 服务日志
sudo journalctl -u stock-monitor -f

# Docker 日志
docker logs -f stock-monitor
```

### 备份数据

```bash
# 备份配置文件
tar -czf config-backup-$(date +%Y%m%d).tar.gz config/

# 备份数据
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/
```

### 更新项目

```bash
# Git 更新
git pull origin main
pip install -r requirements.txt
sudo systemctl restart stock-monitor
```

---

## 故障排查

### Web 服务无法启动

```bash
# 检查端口占用
lsof -i :5000

# 检查日志
tail -f logs/*.log
```

### 飞书推送失败

```bash
# 检查配置
cat config/feishu_config.json

# 测试连接
python -c "import requests; print(requests.get('https://open.feishu.cn').status_code)"
```

### 定时任务不执行

```bash
# 检查 cron 状态
systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog

# 测试脚本
python scripts/multi_stocks_monitor.py
```

---

## 性能优化

### 使用 Redis 缓存

```bash
# 安装 Redis
sudo apt install redis-server

# 安装 Python 客户端
pip install redis

# 修改代码使用缓存
```

### 使用 Gunicorn 多 worker

```bash
gunicorn -w 4 -k gthread -b 0.0.0.0:5000 app:app
```

### 数据库优化

```bash
# 使用 PostgreSQL 替代 SQLite
pip install psycopg2-binary
```

---

_部署问题？查看 [QUICKSTART.md](QUICKSTART.md) 或提 Issue。_
