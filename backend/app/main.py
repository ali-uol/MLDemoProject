import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.services.prediction_service import PredictionService
from src.config import ROOT

def create_app(artifact_root=ROOT) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app):
        logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
        app.state.service = PredictionService(artifact_root)
        app.state.service.load()
        yield
    app = FastAPI(title='Iris Flower Classification',version='1.0.0',lifespan=lifespan)
    app.add_middleware(CORSMiddleware,allow_origins=os.getenv('CORS_ORIGINS','http://localhost:5173,http://127.0.0.1:5173').split(','),
                       allow_methods=['GET','POST'],allow_headers=['Content-Type'])
    @app.exception_handler(RequestValidationError)
    async def invalid_input(request, error):
        # Omit raw inputs: NaN/Infinity cannot be serialized in JSON error responses.
        errors = [{'loc':list(item['loc']),'msg':item['msg'],'type':item['type']} for item in error.errors()]
        return JSONResponse(status_code=422,content={'detail':errors})
    app.include_router(router)
    return app
app = create_app()
