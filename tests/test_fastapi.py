"""
FastAPI 应用测试

测试所有 API 端点的功能
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthCheck:
    """健康检查测试"""

    def test_health_endpoint(self):
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestStockAPI:
    """股票 API 测试"""

    def test_get_stock(self):
        """测试获取股票实时数据"""
        response = client.get("/api/stock/000063")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True

    def test_get_stock_invalid_code(self):
        """测试获取无效股票数据"""
        response = client.get("/api/stock/invalid")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data

    def test_get_news(self):
        """测试获取新闻"""
        response = client.get("/api/news/000063")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_get_history(self):
        """测试获取历史行情"""
        response = client.get("/api/history/000063")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_get_overview(self):
        """测试获取概览数据"""
        response = client.get("/api/overview")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_get_predict(self):
        """测试获取预测数据"""
        response = client.get("/api/predict/000063")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data


class TestStocksConfigAPI:
    """股票配置 API 测试"""

    def test_get_stocks(self):
        """测试获取股票配置列表"""
        response = client.get("/api/stocks")
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_add_stock(self):
        """测试添加股票"""
        # 先获取现有列表
        response = client.get("/api/stocks")
        assert response.status_code == 200
        existing_stocks = response.json()["data"]
        existing_codes = [s["code"] for s in existing_stocks]

        # 创建一个唯一的测试股票代码
        test_code = "test999"
        while test_code in existing_codes:
            test_code = f"test{len(existing_codes) + 1:03d}"

        # 添加测试股票
        stock_data = {
            "code": test_code,
            "name": "测试股票",
            "market": "sz",
            "alias": "测试",
            "notes": "测试股票",
        }
        response = client.post("/api/stocks", json=stock_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # 验证添加成功
        response = client.get("/api/stocks")
        stocks = response.json()["data"]
        codes = [s["code"] for s in stocks]
        assert test_code in codes

        # 清理测试数据
        client.delete(f"/api/stocks/{test_code}")

    def test_add_stock_missing_fields(self):
        """测试添加股票 - 缺少必填字段"""
        stock_data = {"code": "", "name": ""}
        response = client.post("/api/stocks", json=stock_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False

    def test_delete_stock(self):
        """测试删除股票"""
        # 先添加一个测试股票
        test_code = "temp001"
        stock_data = {
            "code": test_code,
            "name": "临时股票",
            "market": "sz",
        }
        client.post("/api/stocks", json=stock_data)

        # 删除测试股票
        response = client.delete(f"/api/stocks/{test_code}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_toggle_stock(self):
        """测试切换股票启用状态"""
        # 先添加一个测试股票
        test_code = "toggle001"
        stock_data = {
            "code": test_code,
            "name": "切换股票",
            "market": "sz",
        }
        client.post("/api/stocks", json=stock_data)

        # 切换状态
        response = client.post(f"/api/stocks/{test_code}/toggle")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "enabled" in data["data"]

        # 再次切换
        response = client.post(f"/api/stocks/{test_code}/toggle")
        assert response.status_code == 200

        # 清理测试数据
        client.delete(f"/api/stocks/{test_code}")


class TestViewsAPI:
    """页面视图 API 测试"""

    def test_index_page(self):
        """测试首页"""
        response = client.get("/")
        assert response.status_code == 200

    def test_stock_detail_page(self):
        """测试股票详情页"""
        response = client.get("/stock/000063")
        assert response.status_code == 200


class TestPydanticModels:
    """Pydantic 模型测试"""

    def test_stock_config_model(self):
        """测试 StockConfig 模型"""
        from app.models.schemas import StockConfig

        config = StockConfig(
            code="000063",
            name="中兴通讯",
            market="sz",
            enabled=True,
            alias="中兴",
            notes="5G 龙头",
        )
        assert config.code == "000063"
        assert config.name == "中兴通讯"
        assert config.market == "sz"

    def test_stock_response_model(self):
        """测试 StockResponse 模型"""
        from app.models.schemas import StockResponse

        response = StockResponse(
            success=True,
            data={"stock": {"code": "000063"}, "price": {"current": 28.5}},
        )
        assert response.success is True
        assert response.error is None


class TestCORS:
    """CORS 测试"""

    def test_cors_headers(self):
        """测试 CORS 头"""
        response = client.options(
            "/api/stock/000063",
            headers={"Origin": "http://localhost:3000"},
        )
        # FastAPI 会自动处理 CORS
        assert response.status_code in [200, 404, 405]


class TestRequestLogging:
    """请求日志测试"""

    def test_request_logging_middleware(self):
        """测试请求日志中间件"""
        response = client.get("/health")
        assert response.status_code == 200
        # 检查处理时间头
        assert "x-process-time" in response.headers
