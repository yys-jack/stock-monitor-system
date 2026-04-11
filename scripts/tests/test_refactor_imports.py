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
        """验证 app.api.api 模块使用 src 导入"""
        # 这个测试会先失败，因为我们还没有修改导入
        # 重构完成后应该通过
        import app.api.api as api_module

        # 检查模块是否成功导入（没有 ImportError）
        assert api_module is not None
        assert hasattr(api_module, 'router')

    def test_app_api_direct_src_import(self):
        """验证 app.api.api 可以直接从 src 导入（重构后的目标）"""
        # 这个测试现在会失败，因为 api.py 仍然从 app.services 导入
        # 我们需要检查 api.py 文件的导入语句
        with open('app/api/api.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # 重构后应该包含这些导入
        assert 'from src import config_loader, stock_service' in content or \
               'from src.config_loader import' in content
