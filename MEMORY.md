# 📋 开发规范（必须遵守）

**最后更新：** 2026-03-26 21:55  
**核心原则：** 配置即代码，重构要完整，监控需先行，定期清理

---

## 🚨 血泪教训（按主题分类）

### Git 流程
| 案例 | 问题 | 教训 |
|------|------|------|
| #1 | 直接在 main 分支开发 | 必须 `git checkout -b feature/xxx` |
| #3 | 推送后才创建分支 | 分支必须在开发前创建 |
| #5 | 文档更新未走 PR | 规范是铁律，无例外 |

### 文档规范
| 案例 | 问题 | 教训 |
|------|------|------|
| #2 | 提交代码未同步文档 | 代码和文档必须一起提交 |
| #5 | 觉得"只是文档"就放松 | 文档变更同样需要 PR |

### 重构规范
| 案例 | 问题 | 教训 |
|------|------|------|
| #4 | 26 文件重构未 TDD，PR 过大 | 测试先行，大重构拆分 PR |
| #6 | 脚本移动但 crontab 未更新 | **配置即代码，重构要完整** |

### 项目维护
| 案例 | 问题 | 教训 |
|------|------|------|
| #7 | 临时文档积累过多 | 定期清理过时文件，保留重要复盘文档 |

---

## 📜 铁律（6 条）

- ❌ 禁止直接在 main 分支开发
- ❌ 禁止跳过 PR 审查
- ❌ 禁止未测试先行就开发
- ❌ 禁止单 PR 过大（>10 文件需拆分）
- ❌ 禁止提交后不同步文档
- ❌ 禁止重构后不更新外部配置

---

## 🔄 开发流程（12 步）

```
1. 文档先行     → AGILE_DEVELOPMENT.md 添加 Sprint 记录
2. 创建分支     → git checkout -b feature/xxx
3. 编写测试     → pytest 测试（预期失败）
4. 运行测试红   → 确认测试失败
5. 代码开发     → 在功能分支上编写
6. 运行测试绿   → 确认测试通过
7. 重构优化     → 保持测试通过
8. 功能测试     → 单元/集成/数据验证
9. 检查 PR 拆分 → >10 文件？拆分多个 PR
10. 提交分支    → git push -u origin feature/xxx
11. PR 审查     → GitHub 创建 Pull Request
12. 同步文档    → README/ROADMAP/AGILE/TESTING
```

---

## ✅ 检查清单

### 推送前检查
```bash
git branch          # ✅ 在 feature/* 分支
git status          # ✅ 没有未提交的更改
git log --oneline -1  # ✅ commit message 规范
pytest              # ✅ 所有测试通过
```

### 重构后检查
```bash
# 配置文件
grep -r "旧路径" config/ scripts/ *.sh
crontab -l | grep "旧路径"

# 部署脚本
grep -r "旧路径" deploy/ .github/ scripts/

# 文档引用
grep -r "旧路径" *.md docs/
```

**检查项：**
- [ ] Crontab 配置已更新
- [ ] Systemd 服务文件已更新
- [ ] 部署脚本已更新
- [ ] 文档引用已更新
- [ ] 监控告警规则已更新
- [ ] 日志路径已验证

### 定期清理检查（每季度）
```bash
# 临时文件
find . -name "*.log" -o -name "*.tmp" -o -name "__pycache__"
find . -name "output" -type d

# 过时文档
ls -la *.md | grep -E "(TEMP|tmp|test|verify)"

# 废弃脚本
ls -la *.sh | grep -E "install_"
```

**清理项：**
- [ ] `__pycache__` 目录
- [ ] `*.log` 日志文件
- [ ] `output/` 临时输出目录
- [ ] 临时验证文档（VERIFY_*.md）
- [ ] 临时测试报告（TEST_REPORT.md）
- [ ] 废弃脚本（已被替代的旧脚本）
- [ ] venv/ 环境目录（.gitignore 已排除）

**保留项：**
- ✅ 重要复盘文档（POSTMORTEM_*.md）
- ✅ 问题调查报告（*_INVESTIGATION_REPORT.md）
- ✅ 开发规范（MEMORY.md）
- ✅ 技术文档（TECH_STACK.md, TESTING.md）

---

## 📝 文档同步规范

| 文档 | 更新内容 | 时机 |
|------|---------|------|
| `AGILE_DEVELOPMENT.md` | Sprint 记录、测试指标 | 代码提交前 |
| `README.md` | 功能说明、使用方法 | 代码提交前 |
| `ROADMAP.md` | 版本发布记录 | 代码提交前 |
| `MEMORY.md` | 违规案例、经验教训 | 事件复盘后 |

**Commit Message 格式：** `<type>: <description>`  
**类型：** `feat` `fix` `docs` `refactor` `test` `chore`

---

## 💡 记住

- 规范不是束缚，是保证质量的工具
- 走捷径最终会走更远的路
- 每次违规都是学习机会
- 自律才能自由

---

## 📅 规范维护

**每次违规后：** 记录案例 → 更新本文档 → 提交 git → 制定改进措施

**配置管理：**
- Crontab 配置模板化：`config/crontab.template`
- 部署脚本：`scripts/install_crontab.sh`
- 配置变更必须通过 PR 审查
