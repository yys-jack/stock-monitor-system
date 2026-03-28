#!/usr/bin/env python3
"""
配置加载器测试
"""

import sys
import unittest
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from config_loader import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    """配置加载器测试类"""

    def setUp(self):
        """测试前准备"""
        self.loader = ConfigLoader()

    def test_load_stocks_config(self):
        """测试加载股票配置"""
        config = self.loader.load_stocks_config()
        self.assertIsNotNone(config)
        self.assertIn("stocks", config)
        self.assertIn("settings", config)

    def test_load_feishu_config(self):
        """测试加载飞书配置"""
        config = self.loader.load_feishu_config()
        # 配置文件可能不存在，返回 None 是正常的
        if config:
            self.assertIn("user_id", config)

    def test_get_env(self):
        """测试获取环境变量"""
        # 设置测试环境变量
        import os

        os.environ["TEST_VAR"] = "test_value"

        value = self.loader.get_env("TEST_VAR")
        self.assertEqual(value, "test_value")

        default = self.loader.get_env("NON_EXISTENT", "default")
        self.assertEqual(default, "default")

    def test_get_env_bool(self):
        """测试获取布尔环境变量"""
        import os

        os.environ["BOOL_TRUE"] = "true"
        os.environ["BOOL_FALSE"] = "false"

        self.assertTrue(self.loader.get_env_bool("BOOL_TRUE"))
        self.assertFalse(self.loader.get_env_bool("BOOL_FALSE"))
        self.assertFalse(self.loader.get_env_bool("NON_EXISTENT"))


if __name__ == "__main__":
    unittest.main()
