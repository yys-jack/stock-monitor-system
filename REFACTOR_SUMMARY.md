# 保守清理重构总结

**日期：** 2026-04-11

## 重构目标

清理项目中的重复代码，统一架构分层，提升可维护性。

## 执行内容

### 1. 归档 webapp 目录
- 将旧 Flask 应用移至 `archive/webapp-old/`
- 保留作为参考，不参与运行

### 2. 删除 app/services
- 服务层统一使用 `src/`
- 简化导入路径

### 3. 重构 scripts
- 移除内联飞书推送代码
- 使用 `src/feishu.py` 统一实现

### 4. 拆分 API 路由
- `app/api/api.py` (325 行) → 3 个独立模块
- `stock_routes.py`: 股票行情相关
- `predict_routes.py`: 预测相关
- `config_routes.py`: 配置管理相关

## 代码减少统计

| 类型 | 减少行数 |
|------|---------|
| webapp/ | ~500 |
| app/services/ | ~150 |
| scripts 内联代码 | ~400 |
| **总计** | **~1050 行** |

## 验证命令

```bash
# 运行所有测试
python -m pytest scripts/tests/ tests/ -v

# 启动 Web 服务
uvicorn app.main:app --reload

# 验证导入
python -c "from src import stock_service, feishu; print('OK')"
```
