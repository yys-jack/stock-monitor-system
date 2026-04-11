#!/usr/bin/env python3
"""
重构验证测试
确保从 app.services 迁移到 src 后导入仍然工作
"""

import pytest


class TestImportRefactor:
    """测试导入路径重构"""

    def test_src_config_loader_exists(self):
        """验证 src.config_loader 模块存在"""
        from src import config_loader
        assert config_loader is not None
        assert hasattr(config_loader, 'load_stocks_config')

    def test_src_stock_service_exists(self):
        """验证 src.stock_service 模块存在"""
        from src import stock_service
        assert stock_service is not None
        assert hasattr(stock_service, 'fetch_stock_price')

    def test_src_feishu_notifier_exists(self):
        """验证 src.feishu 模块存在"""
        from src import feishu
        assert feishu is not None
        assert hasattr(feishu, 'FeishuNotifier')
        assert hasattr(feishu, 'notifier')

    def test_app_api_uses_src_imports(self):
        """验证 app.api 子模块使用 src 导入"""
        # 新的架构中，api.py 是路由聚合器，实际导入在各子模块
        import app.api.stock_routes as stock_module
        import app.api.predict_routes as predict_module
        import app.api.config_routes as config_module

        # 检查各子模块是否成功导入
        assert stock_module is not None
        assert predict_module is not None
        assert config_module is not None

        # 检查是否有 router 属性
        assert hasattr(stock_module, 'router')
        assert hasattr(predict_module, 'router')
        assert hasattr(config_module, 'router')

    def test_app_api_direct_src_import(self):
        """验证 app.api 子模块可以直接从 src 导入（重构后的目标）"""
        # 检查 stock_routes.py 的导入语句
        with open('app/api/stock_routes.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # 重构后应该包含从 src 的导入
        assert 'from src import' in content or 'from src.' in content
