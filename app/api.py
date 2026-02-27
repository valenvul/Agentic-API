import json
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from sklearn.ensemble import RandomForestRegressor
import numpy as np

from app import __version__, schemas
from app.config import settings

api_router = APIRouter()

# Train a dummy model at startup
model_version = "1.0.0"
_model = RandomForestRegressor(n_estimators=10, random_state=42)
_model.fit([[1], [2], [3], [4]], [2, 4, 6, 8])


@api_router.get("/health")
## aca definis el handler del endpoint
def health() -> dict:
    """
    Root Get
    """
    health = schemas.HealthResponse(
        name=settings.PROJECT_NAME, api_version=__version__, model_version=model_version
    )

    return health.dict()


@api_router.post("/prediction", response_model=schemas.PredictionResponse)
def predict(input: schemas.PredictionRequest) -> schemas.PredictionResponse:
    """
    Make a prediction using the dummy random forest model.
    """
    features = np.array(input.features).reshape(1, -1)
    prediction = _model.predict(features)[0]
    return schemas.PredictionResponse(prediction=float(prediction))
