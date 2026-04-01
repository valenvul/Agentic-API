def test_predict_200_correct_input(client):
    response = client.post("/api/v1/predict", json={"features": [0.5]})
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], float)

def test_predict_422_empty_list(client):
    response = client.post("/api/v1/predict", json={"features": []})
    assert response.status_code == 422
    
def test_predict_422_incorrect_values(client):
    response = client.post("/api/v1/predict", json={"features": [9]})
    assert response.status_code == 422

def test_predict_422_missing_features(client):
    response = client.post("/api/v1/predict", json={})
    assert response.status_code == 422

