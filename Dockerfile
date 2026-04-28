FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && chown -R appuser:appuser /app

# 1. Inicializa E exporta o frontend (gera os assets estáticos)
RUN reflex init
RUN reflex export --frontend-only --no-zip

EXPOSE 8080

USER appuser

# 2. Roda backend + serve o frontend estático já buildado
ENTRYPOINT ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--backend-port", "8080"]