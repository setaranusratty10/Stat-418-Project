# syntax=docker/dockerfile:1
FROM python:3.11-slim

# ----- OS deps (optional) -----
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libfreetype6-dev && \
    rm -rf /var/lib/apt/lists/*

# ----- Python deps -----
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----- App code -----
COPY . .

# Cloud Run will override PORT, but we set default for local run
ENV PORT=8000
EXPOSE 8000

CMD ["python", "-m", "shiny", "run", \
     "--host", "0.0.0.0", "--port", "8000", "app.py"]

