from pydantic import BaseModel, field_validator
from typing import List


class PredictionRequest(BaseModel):
    features: List[float]

    @field_validator("features")
    @classmethod
    def validate_features(cls, v: List[float]) -> List[float]:
        if len(v) == 0:
            raise ValueError("features list cannot be empty")
        for i in v:
            if i < 0 or i > 1:
                raise ValueError("features must be between 0 and 1")
        return v


class PredictionResponse(BaseModel):
    prediction: float
