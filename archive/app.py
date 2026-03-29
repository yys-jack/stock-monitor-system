#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控系统 Web 应用入口
Flask 应用工厂模式
"""

from flask import Flask


def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    
    # 配置
    app.config['JSON_AS_ASCII'] = False  # 支持中文 JSON
    
    # 注册蓝图
    from webapp.routes.api import api
    from webapp.routes.views import views
    
    app.register_blueprint(api)
    app.register_blueprint(views)
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'error': 'Not Found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'success': False, 'error': 'Internal Server Error'}, 500
    
    return app


# 创建应用实例
app = create_app()


if __name__ == '__main__':
    print("🦞 股票监控系统 Web 界面启动")
    print("=" * 60)
    print("访问地址：http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
