from unittest.mock import patch, AsyncMock

def test_rag_200(client):
    with patch("app.api.chain") as mock_chain: 
        mock_chain.ainvoke = AsyncMock(return_value="mock answer")
        response = client.post("api/v1/rag", json={"question": "mock question"})

        assert response.status_code == 200
        assert response.json() == {"answer": "mock answer"}
        mock_chain.ainvoke.assert_called_once_with("mock question")

def test_rag_422_missing_question(client):
    with patch("app.api.chain") as mock_chain:
        mock_chain.ainvoke = AsyncMock(return_value="mock answer")
        response = client.post("api/v1/rag", json={})

    assert response.status_code == 422

def test_rag_422_empty_body(client):
    with patch("app.api.chain") as mock_chain:
        mock_chain.ainvoke = AsyncMock(return_value="mock answer")
        response = client.post("api/v1/rag", json=None)

    assert response.status_code == 422

def test_rag_500_chain_fails(client):
    with patch("app.api.chain") as mock_chain:
        mock_chain.ainvoke = AsyncMock(side_effect=Exception("Ollama unavailable"))
        response = client.post("api/v1/rag", json={"question": "mock question"})

    assert response.status_code == 500