# Architecture

## Project Structure

```
app/
├── __init__.py          # App version
├── main.py              # FastAPI app, middleware, router registration
├── api.py               # Route handlers and ML model
├── config.py            # Settings, logging setup
└── schemas/
    ├── __init__.py      # Exports all schemas
    ├── health.py        # HealthResponse schema
    └── prediction.py    # PredictionRequest / PredictionResponse schemas
docs/
├── architecture.md      # This file
└── logging.md           # Logging setup explained
requirements.txt
```

---

## App Initialization Flow

When the server starts, this is the order of execution:

1. `config.py` is imported — `Settings` and `LoggingSettings` are instantiated
2. `main.py` calls `setup_app_logging()` before anything else, so all subsequent logs go through Loguru
3. The `FastAPI` app is created with the project name and OpenAPI URL from settings
4. The HTTP middleware is registered
5. Routers are registered: `api_router` under `/api/v1`, `root_router` at `/`
6. `api.py` trains the dummy Random Forest model once at import time

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | HTML index page |
| `GET` | `/api/v1/health` | Returns app name, API version, and model version |
| `POST` | `/api/v1/prediction` | Accepts features and returns a model prediction |

### GET /api/v1/health

Returns the current state of the service. Useful for uptime monitoring and deployment checks.

**Response:**
```json
{
  "name": "Agentic API",
  "api_version": "0.1.0",
  "model_version": "1.0.0"
}
```

### POST /api/v1/prediction

Runs the input through the Random Forest model and returns a prediction.

**Request:**
```json
{
  "features": [0.5]
}
```

**Response:**
```json
{
  "prediction": 1.0
}
```

**Validation rules:**
- `features` cannot be empty
- Each value must be between `0` and `1`

**Error response (422):**
```json
{
  "detail": [
    {
      "msg": "Value error, features must be between 0 and 1"
    }
  ]
}
```

---

## Schemas

Schemas are defined with Pydantic and serve as the data contracts for the API.

### PredictionRequest
| Field | Type | Validation |
|---|---|---|
| `features` | `List[float]` | Non-empty, all values between 0 and 1 |

### PredictionResponse
| Field | Type |
|---|---|
| `prediction` | `float` |

### HealthResponse
| Field | Type |
|---|---|
| `name` | `str` |
| `api_version` | `str` |
| `model_version` | `str` |

---

## ML Model

The model is a `RandomForestRegressor` from scikit-learn, trained on dummy data at startup:

```python
_model = RandomForestRegressor(n_estimators=10, random_state=42)
_model.fit([[1], [2], [3], [4]], [2, 4, 6, 8])
```

It expects exactly **1 feature** per request. The `random_state=42` ensures the model behaves consistently across restarts.

In a real project this would be replaced by loading a pre-trained model from disk or a model registry.

---

## Configuration

Settings are defined in `config.py` using `pydantic-settings`:

| Setting | Default | Description |
|---|---|---|
| `API_V1_STR` | `/api/v1` | Base path for all API routes |
| `PROJECT_NAME` | `Agentic API` | Displayed in health endpoint and OpenAPI docs |
| `logging.LOGGING_LEVEL` | `INFO` | Log level for Loguru and uvicorn |
