from app.services.prediction_service import PredictionService
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.schemas.prediction import PredictionRequest, PredictionResponse, HealthResponse, ModelInfo, MetricsResponse
router = APIRouter(prefix='/api')
def service(request: Request) -> PredictionService:
    value: PredictionService = request.app.state.service
    if value.model is None: raise HTTPException(503, 'Model unavailable. Check models/iris_decision_tree.joblib and models/model_metadata.json, then restart the backend.')
    return value
@router.get('/health',response_model=HealthResponse)
def health(request: Request):
    loaded = request.app.state.service.model is not None
    return JSONResponse({'status':'healthy' if loaded else 'unavailable','model_loaded':loaded}, status_code=200 if loaded else 503)
@router.post('/predict',response_model=PredictionResponse)
def predict(inputs: PredictionRequest, request: Request):
    return service(request).predict(inputs.model_dump())
@router.get('/model/info',response_model=ModelInfo)
def info(request: Request): return service(request).metadata
@router.get('/model/metrics',response_model=MetricsResponse)
def metrics(request: Request):
    saved_metrics = service(request).metrics
    if saved_metrics is None:
        raise HTTPException(503, 'Saved evaluation metrics are unavailable.')
    return saved_metrics
@router.get('/model/feature-importance',response_model=dict[str,float])
def feature_importance(request: Request): return service(request).feature_importance()
