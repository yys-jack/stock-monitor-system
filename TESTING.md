# 🧪 测试规范

> **Stock Monitor System** 测试流程与规范

**版本：** v5.0  
**最后更新：** 2026-03-25  
**状态：** 📋 规范制定中

---

## 🎯 测试原则

### 测试先行（TDD）✅

**红 - 绿 - 重构循环：**

1. 🔴 **红：** 先写失败的测试用例
2. 🟢 **绿：** 编写最少代码使测试通过
3. 🔄 **重构：** 优化代码，保持测试通过

**示例流程：**
```python
# 1. 先写测试（tests/test_stock_service.py）
def test_fetch_stock_price():
    service = StockService()
    result = service.fetch_stock_price("000063", "sz")
    assert result is not None
    assert result['current'] > 0

# 2. 运行测试（预期失败）
pytest tests/test_stock_service.py  # ❌ FAILED

# 3. 实现功能（webapp/services/stock_service.py）
class StockService:
    def fetch_stock_price(self, code, market):
        # ... 实现代码

# 4. 再次运行测试（应该通过）
pytest tests/test_stock_service.py  # ✅ PASSED
```

---

## 📁 测试目录结构

```
stock-monitor-system/
├── tests/                      # 测试目录 ⭐新增
│   ├── __init__.py
│   ├── conftest.py             # pytest 配置
│   ├── test_stock_service.py   # 股票服务测试
│   ├── test_gold_service.py    # 黄金服务测试
│   ├── test_predictor.py       # 预测服务测试
│   ├── test_config_loader.py   # 配置加载测试
│   ├── test_feishu.py          # 飞书推送测试
│   └── test_api.py             # API 集成测试
├── webapp/
│   └── services/
├── scripts/
└── ...
```

---

## 🧰 测试工具

### pytest 配置

**安装：**
```bash
pip install pytest pytest-cov pytest-flask
```

**pytest.ini：**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --cov=webapp --cov-report=html
```

**conftest.py：**
```python
import pytest
from app import app

@pytest.fixture
def client():
    """Flask 测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_stock():
    """示例股票数据"""
    return {
        "code": "000063",
        "name": "中兴通讯",
        "market": "sz"
    }
```

---

## 📝 测试用例模板

### 单元测试

```python
# tests/test_stock_service.py
import pytest
from webapp.services.stock_service import StockService

class TestStockService:
    """股票服务测试"""
    
    def setup_method(self):
        """每个测试前执行"""
        self.service = StockService()
    
    def test_fetch_stock_price_success(self):
        """测试获取股价成功"""
        result = self.service.fetch_stock_price("000063", "sz")
        
        assert result is not None
        assert result['code'] == '000063'
        assert result['current'] > 0
        assert -10 <= result['change_pct'] <= 10
    
    def test_fetch_stock_price_invalid_code(self):
        """测试无效股票代码"""
        result = self.service.fetch_stock_price("invalid", "sz")
        assert result is None
    
    def test_fetch_news(self):
        """测试获取新闻"""
        news = self.service.fetch_news("000063", limit=5)
        
        assert isinstance(news, list)
        assert len(news) <= 5
```

### 集成测试

```python
# tests/test_api.py
import pytest
from webapp.utils.config_loader import load_stocks_config

class TestStockAPI:
    """股票 API 集成测试"""
    
    def test_get_stock_price(self, client):
        """测试获取股价 API"""
        response = client.get('/api/stock/000063')
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['success'] is True
        assert 'price' in data['data']
    
    def test_get_stocks_list(self, client):
        """测试获取股票列表 API"""
        response = client.get('/api/stocks')
        data = response.get_json()
        
        assert response.status_code == 200
        assert isinstance(data['data'], list)
    
    def test_add_stock(self, client):
        """测试添加股票 API"""
        new_stock = {
            "code": "000001",
            "name": "平安银行",
            "market": "sz"
        }
        
        response = client.post('/api/stocks', json=new_stock)
        data = response.get_json()
        
        assert response.status_code == 201
        assert data['success'] is True
```

---

## 📊 测试覆盖率要求

| 模块 | 最低覆盖率 | 当前 | 状态 |
|------|-----------|------|------|
| **services/** | 80% | 0% | ❌ 待添加 |
| **utils/** | 80% | 0% | ❌ 待添加 |
| **routes/** | 70% | 0% | ❌ 待添加 |
| **scripts/** | 60% | 0% | ❌ 待添加 |
| **总体** | 75% | 0% | ❌ 待添加 |

---

## 🔄 CI/CD 集成

### GitHub Actions 配置

**.github/workflows/test.yml：**
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest --cov=webapp --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

## ✅ 测试检查清单

### 开发前
- [ ] 阅读测试规范
- [ ] 准备测试数据
- [ ] 搭建测试环境

### 开发中
- [ ] 先写测试用例（TDD）
- [ ] 运行测试（预期失败）
- [ ] 实现功能
- [ ] 运行测试（应该通过）

### 提交前
- [ ] 运行所有测试
- [ ] 检查测试覆盖率
- [ ] 确保无失败测试
- [ ] 更新测试报告

### PR 审查
- [ ] 测试用例完整
- [ ] 覆盖率达到要求
- [ ] 测试代码规范
- [ ] 无硬编码数据

---

## 📚 参考资料

- [pytest 官方文档](https://docs.pytest.org/)
- [Flask 测试文档](https://flask.palletsprojects.com/testing/)
- [测试驱动开发（TDD）](https://en.wikipedia.org/wiki/Test-driven_development)

---

## 🎯 下一步计划

### Sprint 6 - 测试框架搭建（计划中）

**任务清单：**
- [ ] 添加 pytest 依赖
- [ ] 创建 tests/ 目录结构
- [ ] 编写 conftest.py 配置
- [ ] 实现核心服务测试（stock/gold/predictor）
- [ ] 配置 GitHub Actions CI
- [ ] 设置覆盖率阈值（75%）

**预计工时：** 3 小时  
**优先级：** P1

---

**规范维护：** 每次测试流程优化后更新本文档  
**最后更新：** 2026-03-25 22:00  
**制定者：** 派大星
