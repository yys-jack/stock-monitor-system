# 贡献指南

欢迎贡献代码！

## 贡献流程

### 1. Fork 并克隆

```bash
git clone https://github.com/YOUR_USERNAME/stock-monitor-system.git
cd stock-monitor-system
```

### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 3. 开发

```bash
# 安装开发依赖
make dev

# 运行测试和检查
make test
make lint
```

### 4. 提交

```bash
git add .
git commit -m "feat: 添加新功能"
```

**提交规范:**
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/配置

### 5. 推送 PR

```bash
git push origin feature/your-feature-name
```

在 GitHub 上创建 Pull Request。

---

## 代码规范

- 遵循 PEP 8
- 使用 Black 格式化
- 使用 Ruff 检查
- 使用类型提示

```bash
black scripts/ webapp/
ruff check scripts/ webapp/
```

---

## 测试要求

- 新功能必须包含测试
- 现有测试必须通过

```bash
make test
```

---

## PR 检查清单

- [ ] 代码通过测试
- [ ] 代码已格式化
- [ ] 代码通过检查
- [ ] 添加了测试
- [ ] 更新了文档

---

## 开发规范

详见：[CLAUDE.md](../../.claude/CLAUDE.md)

### Git 工作流

```bash
# 1. 创建分支
git checkout -b feature/xxx

# 2. 开发 + 测试
# 编写代码 → 运行测试 → 通过

# 3. 提交
git add .
git commit -m "feat: 描述"
git push -u origin feature/xxx

# 4. PR 审查
# GitHub 创建 Pull Request

# 5. 合并
# 审查通过后合并到 main
```

### Commit 规范

格式：`<type>: <description>`

| 类型 | 说明 |
|------|------|
| `feat:` | 新功能 |
| `fix:` | Bug 修复 |
| `docs:` | 文档更新 |
| `refactor:` | 重构 |
| `test:` | 测试 |
| `chore:` | 配置/工具 |

---

**问题反馈:** [GitHub Issues](https://github.com/yys-jack/stock-monitor-system/issues)
