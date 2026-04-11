# 故障排除

## 常见问题

### 飞书推送不工作

**症状：** 收不到飞书消息推送

**原因：** 凭证配置错误

**解决方法：**
1. 检查 `config/feishu_config.json` 中的 `app_id` 和 `app_secret` 是否正确
2. 确认飞书应用已发布
3. 验证用户 ID 是否正确添加

### 股票数据获取失败

**症状：** API 返回空数据或错误

**原因：** 网络问题或 API 不可用

**解决方法：**
1. 确保服务器可访问外网
2. 检查 AkShare 和腾讯财经 API 可用性
3. 查看日志文件：`logs/*.log`

### 模拟交易数据库错误

**症状：** 无法创建订单或查询持仓

**原因：** 数据库表结构问题

**解决方法：**
```bash
# 删除旧数据库
rm data/paper_trading.db

# 重启服务
uvicorn app.main:app --reload
```

### Cron 任务不执行

**症状：** 定时任务未运行

**原因：** Cron 服务未启动或路径错误

**解决方法：**
```bash
# 检查 Cron 服务
systemctl status cron

# 重新安装 Cron 任务
./cron_install.sh uninstall
./cron_install.sh install

# 验证 Python 路径
which python3
```

### Web 界面无法访问

**症状：** 浏览器显示无法连接

**原因：** 服务未启动或端口被占用

**解决方法：**
```bash
# 检查服务是否运行
ps aux | grep uvicorn

# 查看端口占用
lsof -i :8000

# 重启服务
uvicorn app.main:app --reload --port 8001
```

## 日志文件位置

```
logs/
├── push_cron.log      # 股票推送
├── gold_cron.log      # 黄金监控
├── alert_cron.log     # 股价预警
└── app.log            # Web 应用
```

## 获取帮助

- [GitHub Issues](https://github.com/yys-jack/stock-monitor-system/issues)
- [讨论区](https://github.com/yys-jack/stock-monitor-system/discussions)
