#!/usr/bin/env python3
"""
飞书推送服务测试
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.feishu import FeishuNotifier, notifier, send_text, send_post


class TestFeishuNotifier(unittest.TestCase):
    """飞书推送服务测试类"""

    def setUp(self):
        """测试前准备"""
        self.notifier = FeishuNotifier()

    def test_notifier_instance(self):
        """测试通知器实例"""
        self.assertIsNotNone(self.notifier)
        self.assertIsInstance(self.notifier, FeishuNotifier)

    def test_global_notifier(self):
        """测试全局通知器实例"""
        self.assertIsNotNone(notifier)
        self.assertIsInstance(notifier, FeishuNotifier)

    def test_send_text_function(self):
        """测试发送文本函数存在"""
        # 验证函数存在且可调用
        self.assertTrue(callable(send_text))

    def test_send_post_function(self):
        """测试发送 Post 函数存在"""
        # 验证函数存在且可调用
        self.assertTrue(callable(send_post))

    def test_notifier_attributes(self):
        """测试通知器属性"""
        # 验证必要属性存在
        self.assertTrue(hasattr(self.notifier, "enabled"))
        self.assertTrue(hasattr(self.notifier, "user_id"))
        self.assertTrue(hasattr(self.notifier, "app_id"))
        self.assertTrue(hasattr(self.notifier, "app_secret"))
        self.assertTrue(hasattr(self.notifier, "retry_times"))
        self.assertTrue(hasattr(self.notifier, "retry_delay"))

    def test_send_text_message_disabled(self):
        """测试禁用时发送文本消息"""
        # 保存原状态
        original_enabled = self.notifier.enabled
        self.notifier.enabled = False

        # 禁用时应返回 False
        result = self.notifier.send_text_message("test content")
        self.assertFalse(result)

        # 恢复原状态
        self.notifier.enabled = original_enabled

    def test_send_post_message_disabled(self):
        """测试禁用时发送 Post 消息"""
        # 保存原状态
        original_enabled = self.notifier.enabled
        self.notifier.enabled = False

        # 禁用时应返回 False
        result = self.notifier.send_post_message("Test Title", [])
        self.assertFalse(result)

        # 恢复原状态
        self.notifier.enabled = original_enabled

    @patch("src.feishu.requests.post")
    def test_get_access_token_mock(self, mock_post):
        """测试获取访问令牌（模拟）"""
        # 配置 mock 响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 0,
            "tenant_access_token": "test_token",
        }
        mock_post.return_value = mock_response

        # 设置测试凭据
        self.notifier.app_id = "test_app_id"
        self.notifier.app_secret = "test_app_secret"

        # 调用方法
        token = self.notifier._get_access_token()

        # 验证结果
        self.assertEqual(token, "test_token")

    @patch("src.feishu.requests.post")
    def test_get_access_token_failure(self, mock_post):
        """测试获取访问令牌失败（模拟）"""
        # 配置 mock 响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 1000, "message": "error"}
        mock_post.return_value = mock_response

        self.notifier.app_id = "test_app_id"
        self.notifier.app_secret = "test_app_secret"

        token = self.notifier._get_access_token()

        self.assertIsNone(token)

    def test_get_access_token_no_credentials(self):
        """测试无凭据时获取令牌"""
        self.notifier.app_id = ""
        self.notifier.app_secret = ""

        token = self.notifier._get_access_token()

        self.assertIsNone(token)

    def test_send_text_message_no_user(self):
        """测试无用户 ID 时发送文本消息"""
        original_enabled = self.notifier.enabled
        original_user = self.notifier.user_id

        self.notifier.enabled = True
        self.notifier.user_id = ""

        # 无用户 ID 时应返回 False
        result = self.notifier.send_text_message("test content")
        self.assertFalse(result)

        # 恢复
        self.notifier.enabled = original_enabled
        self.notifier.user_id = original_user

    def test_send_post_message_no_user(self):
        """测试无用户 ID 时发送 Post 消息"""
        original_enabled = self.notifier.enabled
        original_user = self.notifier.user_id

        self.notifier.enabled = True
        self.notifier.user_id = ""

        result = self.notifier.send_post_message("Title", [])
        self.assertFalse(result)

        # 恢复
        self.notifier.enabled = original_enabled
        self.notifier.user_id = original_user

    def test_message_content_format(self):
        """测试消息内容格式"""
        # 测试文本消息格式
        text_content = "这是一条测试消息"
        self.assertIsInstance(text_content, str)
        self.assertTrue(len(text_content) > 0)

        # 测试 Post 消息内容格式
        post_content = [
            [{"tag": "text", "text": "第一行"}],
            [{"tag": "text", "text": "第二行"}],
        ]
        self.assertIsInstance(post_content, list)
        self.assertEqual(len(post_content), 2)


if __name__ == "__main__":
    unittest.main()
