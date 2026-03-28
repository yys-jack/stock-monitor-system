# Webapp package
# 注意：webapp 模块已重构，服务层已迁移到 src 模块
# 请使用：from src import StockService, GoldService, StockPredictor, etc.

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
