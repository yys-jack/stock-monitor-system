# 贡献指南

欢迎贡献代码！请遵循以下流程：

## 🌟 贡献流程

### 1. Fork 项目

```bash
# 在 GitHub 上 Fork 项目
# 然后克隆到本地
git clone https://github.com/YOUR_USERNAME/stock-monitor-system.git
cd stock-monitor-system
```

### 2. 创建分支

```bash
# 基于 develop 分支创建功能分支
git checkout develop
git checkout -b feature/your-feature-name
```

### 3. 开发

```bash
# 安装开发依赖
make dev

# 编写代码和测试
# ...

# 运行测试
make test

# 代码检查
make lint
make type-check
```

### 4. 提交代码

```bash
# 添加更改
git add .

# 提交（遵循约定式提交规范）
git commit -m "feat: 添加新功能"
# 或
git commit -m "fix: 修复某个 bug"
# 或
git commit -m "docs: 更新文档"
```

### 5. 推送并创建 PR

```bash
# 推送到远程
git push origin feature/your-feature-name

# 在 GitHub 上创建 Pull Request
```

---

## 📝 提交规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具/配置

**示例：**
```bash
git commit -m "feat: 添加黄金价格预警功能"
git commit -m "fix: 修复股价数据解析错误"
git commit -m "docs: 更新快速开始指南"
```

---

## 🧪 测试要求

- 新功能必须包含测试
- 现有测试必须通过
- 测试覆盖率不应下降

```bash
# 运行测试
make test

# 查看覆盖率报告
open htmlcov/index.html
```

---

## 💻 代码规范

### Python 代码

- 遵循 PEP 8
- 使用 Black 格式化
- 使用 Ruff 检查

```bash
# 格式化代码
black scripts/ webapp/

# 检查代码
ruff check scripts/ webapp/
```

### 类型提示

鼓励使用类型提示：

```python
def fetch_stock_price(code: str, market: str) -> Optional[dict]:
    """获取股票价格"""
    pass
```

---

## 📋 PR 检查清单

创建 PR 前，请确认：

- [ ] 代码已通过测试
- [ ] 代码已格式化（Black）
- [ ] 代码已通过检查（Ruff）
- [ ] 添加了必要的测试
- [ ] 更新了文档
- [ ] 提交信息符合规范

---

## 🐛 报告问题

发现 Bug？请创建 Issue 并提供：

1. 问题描述
2. 复现步骤
3. 预期行为
4. 实际行为
5. 环境信息（Python 版本、OS 等）

---

## 💡 功能建议

有新想法？欢迎创建 Issue 讨论：

- 功能描述
- 使用场景
- 实现思路（可选）

---

## 📞 联系方式

- GitHub Issues: [项目 Issue 页面](https://github.com/yys-jack/stock-monitor-system/issues)
- Email: yys-jack@example.com

---

感谢你的贡献！🎉
