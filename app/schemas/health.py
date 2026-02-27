from pydantic import BaseModel


class HealthResponse(BaseModel):
    name: str
    api_version: str
    model_version: str
