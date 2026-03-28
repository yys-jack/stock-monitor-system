#!/usr/bin/env python3
"""
飞书推送服务
"""

import time
from typing import List, Optional

import requests

try:
    from .config_loader import load_feishu_config
except ImportError:
    from config_loader import load_feishu_config


class FeishuNotifier:
    """飞书通知推送类"""

    def __init__(self):
        config = load_feishu_config()
        feishu_cfg = config.get("feishu", {}) if config else {}

        self.enabled = feishu_cfg.get("enabled", False)
        self.user_id = feishu_cfg.get("user_id", "")
        self.app_id = feishu_cfg.get("app_id", "")
        self.app_secret = feishu_cfg.get("app_secret", "")
        self.retry_times = feishu_cfg.get("retry_times", 3)
        self.retry_delay = feishu_cfg.get("retry_delay_seconds", 2)

        self.access_token: Optional[str] = None
        self.token_expire_time = 0.0

    def _get_access_token(self) -> Optional[str]:
        """获取飞书访问令牌"""
        if not self.app_id or not self.app_secret:
            print("[WARN] 飞书 app_id 或 app_secret 未配置")
            return None

        if self.access_token and time.time() < self.token_expire_time - 300:
            return self.access_token

        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            payload = {"app_id": self.app_id, "app_secret": self.app_secret}

            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()

            data = resp.json()
            if data.get("code") == 0:
                self.access_token = data["tenant_access_token"]
                self.token_expire_time = time.time() + 7200
                return self.access_token
            else:
                print(f"[ERROR] 获取飞书令牌失败：{data}")
                return None

        except Exception as e:
            print(f"[ERROR] 获取飞书令牌异常：{e}")
            return None

    def send_text_message(self, content: str, user_id: Optional[str] = None) -> bool:
        """发送文本消息"""
        if not self.enabled:
            print("[INFO] 飞书推送未启用")
            return False

        token = self._get_access_token()
        if not token:
            return False

        target_user = user_id or self.user_id
        if not target_user:
            print("[ERROR] 飞书 user_id 未配置")
            return False

        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        payload = {"receive_id": target_user, "msg_type": "text", "content": {"text": content}}

        for attempt in range(self.retry_times):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=10)
                resp.raise_for_status()

                data = resp.json()
                if data.get("code") == 0:
                    print("[INFO] 飞书推送成功")
                    return True
                else:
                    print(f"[ERROR] 飞书推送失败：{data}")

            except Exception as e:
                print(f"[ERROR] 飞书推送异常 (尝试 {attempt + 1}/{self.retry_times}): {e}")
                if attempt < self.retry_times - 1:
                    time.sleep(self.retry_delay)

        return False

    def send_post_message(self, title: str, content_list: List) -> bool:
        """发送 Post 消息（富文本）"""
        if not self.enabled:
            print("[INFO] 飞书推送未启用")
            return False

        token = self._get_access_token()
        if not token:
            return False

        target_user = self.user_id
        if not target_user:
            print("[ERROR] 飞书 user_id 未配置")
            return False

        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        post_content = {"zh_cn": {"title": title, "content": content_list}}
        payload = {"receive_id": target_user, "msg_type": "post", "content": post_content}

        for attempt in range(self.retry_times):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=10)
                resp.raise_for_status()

                data = resp.json()
                if data.get("code") == 0:
                    print("[INFO] 飞书 Post 消息推送成功")
                    return True
                else:
                    print(f"[ERROR] 飞书 Post 消息推送失败：{data}")

            except Exception as e:
                print(f"[ERROR] 飞书 Post 消息推送异常 (尝试 {attempt + 1}/{self.retry_times}): {e}")
                if attempt < self.retry_times - 1:
                    time.sleep(self.retry_delay)

        return False


# 全局实例
notifier = FeishuNotifier()


def send_text(content: str, user_id: Optional[str] = None) -> bool:
    """便捷函数：发送文本消息"""
    return notifier.send_text_message(content, user_id)


def send_post(title: str, content_list: List) -> bool:
    """便捷函数：发送 Post 消息"""
    return notifier.send_post_message(title, content_list)
