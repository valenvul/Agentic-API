import json
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()

_model = joblib.load(settings.MODEL_PATH)
model = _model["model"]
model_version = _model["version"]

# the extra params are for documentation
@api_router.get("/health", response_model=schemas.HealthResponse, status_code=200)
## aca definis el handler del endpoint
def health() -> dict:
    """
    Root Get
    """
    health = schemas.HealthResponse(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.model_dump()


@api_router.post("/predict", response_model=schemas.PredictionResponse, status_code=200)
def predict(input: schemas.PredictionRequest) -> schemas.PredictionResponse:
    """
    Make a prediction using the dummy random forest model.
    """
    features = np.array(input.features).reshape(1, -1)
    prediction = model.predict(features)[0]
    return schemas.PredictionResponse(prediction=float(prediction))
