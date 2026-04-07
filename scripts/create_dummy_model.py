import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=1, random_state=0)
model.fit(np.array([[0.5]]), [1.0])
joblib.dump({"model": model, "version": "test"}, "model.pkl")
