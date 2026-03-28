.PHONY: help install dev test lint type-check clean run-web run-monitor run-gold

help:
	@echo "股票监控系统 - Makefile 命令"
	@echo ""
	@echo "安装:"
	@echo "  make install       安装生产环境依赖"
	@echo "  make dev           安装开发环境依赖"
	@echo ""
	@echo "测试:"
	@echo "  make test          运行测试"
	@echo "  make lint          代码风格检查"
	@echo "  make type-check    类型检查"
	@echo ""
	@echo "运行:"
	@echo "  make run-web       启动 Web 界面"
	@echo "  make run-monitor   运行股票监控"
	@echo "  make run-gold      运行黄金监控"
	@echo ""
	@echo "清理:"
	@echo "  make clean         清理缓存和构建文件"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black ruff mypy

test:
	python -m pytest scripts/tests/ -v --cov=scripts --cov-report=html

lint:
	ruff check scripts/ webapp/

type-check:
	mypy scripts/ webapp/ --ignore-missing-imports

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .pytest_cache/ .mypy_cache/
	rm -rf output/*.txt output/*.md
	@echo "清理完成"

run-web:
	python app.py

run-monitor:
	python scripts/multi_stocks_monitor.py

run-gold:
	python scripts/gold_monitor.py
