"""
预测相关 API 路由
"""
from fastapi import APIRouter

from app.models.schemas import PredictReport, PredictResponse
from src.predictor import StockPredictor

router = APIRouter(tags=["Prediction"])


@router.get("/predict/{code}", response_model=PredictResponse)
async def get_predict(code: str) -> PredictResponse:
    """获取预测数据"""
    try:
        predictor = StockPredictor(code)
        result = predictor.predict()
        return PredictResponse(success=True, data=result)
    except Exception as e:
        return PredictResponse(success=False, error=str(e))


@router.get("/predict/report/{code}", response_model=PredictReport)
async def get_predict_report(code: str) -> PredictReport:
    """获取预测报告（文本格式）"""
    try:
        predictor = StockPredictor(code)
        report = predictor.generate_report()
        return PredictReport(success=True, data={"report": report})
    except Exception as e:
        return PredictReport(success=False, error=str(e))
