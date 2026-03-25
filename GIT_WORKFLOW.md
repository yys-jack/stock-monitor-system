## Git 工作流程

### 🌿 分支策略

| 分支 | 用途 | 说明 |
|------|------|------|
| `main` | 主分支 | 生产环境，只接受通过测试的功能合并 |
| `dev` | 开发分支 | 日常开发工作在此分支进行（可选） |
| `feature/*` | 功能分支 | 新增功能时使用 |
| `fix/*` | 修复分支 | Bug 修复时使用 |
| `hotfix/*` | 紧急修复 | 生产环境紧急修复时使用 |

---

## 📋 开发流程（分支模式）

### 模式一：功能分支工作流（推荐）

#### 1️⃣ 创建功能分支
```bash
# 确保基于最新的 main 分支
git checkout main
git pull origin main

# 创建功能分支
git checkout -b feature/功能简述

# 或 Bug 修复分支
git checkout -b fix/问题简述
```

**分支命名规范：**
- `feature/gold-monitor` - 黄金监控功能
- `feature/cron-optimization` - Cron 优化
- `fix/trading-time-check` - 交易时间判断修复
- `fix/push-failure` - 推送失败修复

#### 2️⃣ 开发并测试
```bash
# 编写代码...
# 运行测试...
python3 multi_stocks_monitor.py
```

#### 3️⃣ 提交到功能分支
```bash
git add <modified_files>
git commit -m "<type>: <description>"
git push origin feature/功能简述
```

#### 4️⃣ 创建 Pull Request
- 在 GitHub 上创建 PR：`feature/*` → `main`
- 描述变更内容、测试结果
- 等待审查通过后合并

#### 5️⃣ 删除已合并的分支
```bash
# 本地删除
git branch -d feature/功能简述

# 远程删除
git push origin --delete feature/功能简述
```

---

### 模式二：Git Worktree 工作流（多任务并行）

**适用场景：** 需要同时开发多个功能/修复多个 bug

#### 1️⃣ 添加工作树
```bash
# 为功能 A 创建工作树
git worktree add ../feature-gold feature/gold-monitor

# 为功能 B 创建工作树
git worktree add ../feature-cron feature/cron-optimization

# 为 Bug 修复创建工作树
git worktree add ../fix-push fix/push-failure
```

#### 2️⃣ 在不同工作树间切换
```bash
# 进入工作树目录
cd ../feature-gold

# 正常开发、测试、提交
git add .
git commit -m "feat: 添加黄金监控"
git push origin feature/gold-monitor

# 切换到另一个工作树
cd ../feature-cron
```

#### 3️⃣ 查看工作树状态
```bash
# 列出所有工作树
git worktree list

# 输出示例：
# /path/to/repo              main
# /path/to/feature-gold      feature/gold-monitor
# /path/to/feature-cron      feature/cron-optimization
```

#### 4️⃣ 清理工作树
```bash
# 功能完成后移除工作树
git worktree remove ../feature-gold

# 清理已完成分支
git branch -d feature/gold-monitor
git push origin --delete feature/gold-monitor
```

**优势：**
- ✅ 多个功能并行开发，互不干扰
- ✅ 每个工作树有独立的 git 状态
- ✅ 无需频繁 `git stash` 或切换分支
- ✅ 可以同时测试多个功能

---

## 📝 Commit Message 规范

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat: 添加黄金价格监控` |
| `fix` | Bug 修复 | `fix: 修复交易时间判断逻辑` |
| `docs` | 文档更新 | `docs: 更新 README 使用说明` |
| `refactor` | 代码重构 | `refactor: 优化数据获取逻辑` |
| `test` | 测试相关 | `test: 添加金价数据验证测试` |
| `chore` | 配置/工具 | `chore: 更新 Cron 配置脚本` |

**完整示例：**
```bash
git commit -m "feat: 添加黄金价格监控功能

- 新增 gold_monitor.py 监控脚本
- 添加 gold_config.json 配置文件
- 集成上期所黄金期货数据源
- 支持飞书消息推送

测试：
- ✅ 核心功能测试通过
- ✅ 数据准确性验证（对比支付宝）
- ✅ 推送测试成功"
```

---

## 🔄 完整开发闭环

```
1. 创建分支    → feature/xxx 或 fix/xxx
       ↓
2. 代码开发    → 编写代码 + 自检
       ↓
3. 功能测试    → 单元测试 + 集成测试 + 数据验证
       ↓
4. 提交分支    → git push origin feature/xxx
       ↓
5. 创建 PR     → GitHub 上创建 Pull Request
       ↓
6. 代码审查    → 等待审查意见并修改
       ↓
7. 合并到 main → 审查通过后合并
       ↓
8. 清理分支    → 删除本地和远程分支
```

---

## 💡 最佳实践

### ✅ 推荐做法
- 每个功能/修复使用独立分支
- 分支命名清晰描述用途
- 小步提交，频繁推送
- PR 描述包含测试结果
- 合并后及时删除分支

### ❌ 避免做法
- 直接在 `main` 分支开发
- 一个分支包含多个不相关功能
- 提交信息过于简单（如 "update"）
- 不测试就直接提交
- 长期不删除已合并分支

---

## 🛠️ 常用命令速查

```bash
# 查看当前分支
git branch

# 创建并切换到新分支
git checkout -b feature/新功能

# 查看远程分支
git branch -r

# 拉取最新代码
git pull origin main

# 推送分支到远程
git push -u origin feature/新功能

# 查看工作树
git worktree list

# 添加工作树
git worktree add ../路径 分支名

# 移除工作树
git worktree remove ../路径
```