# 文档整理设计规格

> **Spec Date:** 2026-04-11
> **Status:** Approved

## 目标

重构项目文档结构，实现用户指南与开发文档分离，提升文档可维护性和可读性。

## 设计决策

### 1. 删除内容
- `archive/` 目录完全删除（所有内容已过时）

### 2. 根目录保留
- `README.md` — 精简至 ~100 行
- `CHANGELOG.md` — 保留
- `ROADMAP.md` — 保留

### 3. 新建文档结构

```
docs/
├── guide/                      # 用户指南
│   ├── README.md               # 指南索引
│   ├── quickstart.md           # 5 分钟快速上手
│   ├── deployment.md           # 部署指南
│   ├── config.md               # 配置说明
│   ├── cron.md                 # Cron 定时任务
│   ├── trading.md              # 模拟交易
│   └── troubleshooting.md      # 故障排除（新增）
│
├── dev/                        # 开发文档
│   ├── README.md               # 开发索引
│   ├── setup.md                # 开发环境设置
│   ├── contributing.md         # 贡献指南
│   ├── architecture.md         # 架构说明（新增）
│   └── api.md                  # API 接口文档
│
└── archive/                    # 历史归档
    └── README.md               # 归档说明
```

### 4. 内容迁移

| 来源 | 目标 | 说明 |
|------|------|------|
| `README.md` 快速开始 | `docs/guide/quickstart.md` | 详细步骤 |
| `README.md` 项目结构 | `docs/dev/architecture.md` | 扩展架构图解 |
| `README.md` 核心功能详解 | `docs/guide/` | 拆分到各功能文档 |
| `README.md` Cron 配置 | `docs/guide/cron.md` | 完整迁移 |
| `DEPLOYMENT.md` | `docs/guide/deployment.md` | 扩展内容 |
| `CONTRIBUTING.md` | `docs/dev/contributing.md` | 扩展内容 |
| `archive/*` | 删除 | 内容已过时 |

### 5. README.md 精简后结构

- 项目简介（1 段）
- 徽章（5 个）
- 快速开始（5 行命令）
- 文档索引表格
- 功能概览表格

---

**批准人：** 用户
**批准日期：** 2026-04-11
