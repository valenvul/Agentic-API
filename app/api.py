
from fastapi import APIRouter, HTTPException
import numpy as np
import joblib

from app import __version__, schemas
from app.config import settings
from app.rag import chain

api_router = APIRouter()

_model = joblib.load(settings.MODEL_PATH)
model = _model["model"]
model_version = _model["version"]

# the extra params are for documentation
@api_router.get("/health", response_model=schemas.HealthResponse, status_code=200)
## here is where the handler is defined
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

@api_router.post("/rag", response_model=schemas.RagResponse, status_code=200)
# make this endpoint async so the api doesn't wait for ollama to finish
async def rag(input: schemas.RagRequest) -> schemas.RagResponse:
    """
    Answer a question using the uploaded files.
    """
    try:
        answer = await chain.ainvoke(input.question)
    except Exception:
        raise HTTPException(status_code=500, detail="RAG pipeline failed")
    return schemas.RagResponse(answer=answer)