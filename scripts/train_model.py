import os
import joblib
from sklearn.ensemble import RandomForestRegressor

# Train a dummy model 
model_version = "1.0.0"
_model = RandomForestRegressor(n_estimators=10, random_state=42)
_model.fit([[1], [2], [3], [4]], [2, 4, 6, 8])

# Save model and version together
model_path = os.getenv("MODEL_PATH", "model.pkl")
os.makedirs(os.path.dirname(os.path.abspath(model_path)), exist_ok=True)
joblib.dump({"model": _model, "version": model_version}, model_path)


