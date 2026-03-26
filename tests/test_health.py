from app import __version__


def test_health_200_correct_versions(client, model):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["api_version"] == __version__
    assert response.json()["model_version"] == model["version"]

