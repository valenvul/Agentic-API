FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

FROM python:3.12-slim AS runner
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY app/ ./app/
COPY model.pkl .

ENV MODEL_PATH=/app/model.pkl

EXPOSE 8000

CMD  ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]