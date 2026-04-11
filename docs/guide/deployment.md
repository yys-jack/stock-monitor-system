# 部署指南

## 本地开发环境

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
uvicorn app.main:app --reload
```

## 生产环境部署

### 方案 A: 直接部署

```bash
# 安装依赖
pip install -r requirements.txt
pip install gunicorn

# 配置
vim config/feishu_config.json
vim config/stocks_config.json

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app

# 定时任务
bash cron_install.sh install
```

### 方案 B: Docker 部署

```bash
# 构建镜像
docker build -t stock-monitor-system .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/config:/app/config \
  --name stock-monitor \
  stock-monitor-system
```

### 方案 C: Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

运行：
```bash
docker-compose up -d
```

## Cron 定时任务

```bash
# 安装所有任务
./cron_install.sh install

# 查看状态
./cron_install.sh status

# 卸载任务
./cron_install.sh uninstall
```

详见：[Cron 定时任务](cron.md)

## 验证部署

```bash
# 健康检查
curl http://localhost:8000/health

# 查看日志
tail -f logs/*.log
```
