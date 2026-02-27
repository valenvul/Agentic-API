# AI-Powered Backend Bridge

A personal project to learn how to properly deploy ML models and extend them with agentic capabilities.

---

## Goals

- Serve ML models through a production-ready API with data validation
- Containerize and automate the deployment pipeline (MLOps)
- Give the system knowledge of private documents via RAG
- Add an autonomous agent that can reason and interact with the backend

---

## What's included

| Module | Description |
|---|---|
| ⚙️ ML Backend | FastAPI REST API with input validation and structured prediction contracts |
| 📦 MLOps | Docker containerization and CI/CD via GitHub Actions |
| 🧠 RAG Layer | Vector database (ChromaDB) for document retrieval and grounded responses |
| 🤖 Agentic Layer | LangGraph agent that decides when to predict, retrieve, or respond directly |

---

## How to Run

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Stack

| | |
|---|---|
| Language | Python |
| API Framework | FastAPI |
| AI Orchestration | LangChain / LangGraph |
| Infrastructure | Docker & GitHub Actions |
| Vector Storage | ChromaDB |
