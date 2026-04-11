# 开发环境设置

## 前置要求

- Python 3.8+
- Git
- 代码编辑器（VS Code/PyCharm）

## 克隆项目

```bash
git clone https://github.com/yys-jack/stock-monitor-system.git
cd stock-monitor-system
```

## 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装生产依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest pytest-cov black ruff mypy
# 或
make dev
```

## 代码质量工具

```bash
# 代码风格检查
make lint      # ruff

# 类型检查
make type-check  # mypy

# 运行测试
make test      # pytest
```

## Pre-commit 钩子

```bash
# 安装 pre-commit
pip install pre-commit
pre-commit install

# 手动运行检查
pre-commit run --all-files
```

## 运行开发服务器

```bash
# Web 界面
uvicorn app.main:app --reload

# 访问 http://localhost:8000
```
