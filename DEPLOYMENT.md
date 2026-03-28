# 📦 部署指南

## 本地开发

```bash
# 1. 克隆
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system

# 2. 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置
cp config/feishu_config.example.json config/feishu_config.json
cp .env.example .env

# 5. 运行
python app.py
```

---

## 生产环境

### 方案 A: 直接部署

```bash
# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 配置
vim config/feishu_config.json
vim config/stocks_config.json

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 定时任务
bash cron_install.sh install
```

### 方案 B: Docker

```bash
docker build -t stock-monitor-system .
docker run -d -p 5000:5000 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/logs:/app/logs \
  stock-monitor-system
```

### 方案 C: Docker Compose

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
    restart: unless-stopped
```

```bash
docker-compose up -d
```

---

## Systemd 服务

创建 `/etc/systemd/system/stock-monitor.service`:

```ini
[Unit]
Description=Stock Monitor System
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/stock-monitor-system
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable stock-monitor
sudo systemctl start stock-monitor
```

---

## Nginx 反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 维护

### 查看日志

```bash
tail -f logs/*.log
sudo journalctl -u stock-monitor -f
docker logs -f stock-monitor
```

### 备份

```bash
tar -czf backup-$(date +%Y%m%d).tar.gz config/ data/
```

### 更新

```bash
git pull origin main
pip install -r requirements.txt
sudo systemctl restart stock-monitor
```

---

**更多:** [QUICKSTART.md](QUICKSTART.md) | [README.md](README.md)
