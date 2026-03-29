# 📋 开发规范

## 📜 铁律

- ❌ 禁止直接在 main 分支开发
- ❌ 禁止跳过 PR 审查
- ❌ 禁止未测试就提交
- ❌ 禁止单 PR 过大（>10 文件需拆分）
- ❌ 禁止重构后不更新配置

## 🔄 开发流程

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

## 📝 Commit 规范

**格式:** `<type>: <description>`

**类型:**
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 重构
- `test:` 测试
- `chore:` 配置/工具

**示例:**
```bash
git commit -m "feat: 添加股票预测功能"
git commit -m "fix: 修复股价数据解析错误"
git commit -m "docs: 更新快速开始指南"
```

---

## 💡 核心原则

**分支开发 → 测试先行 → 小步提交 -> 同步修改文档 → PR 审查**

- 规范保证质量，不是束缚
- 配置即代码，重构要完整
- 自律才能自由

---

