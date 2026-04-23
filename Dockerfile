FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl -sL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 1. Inicializa E exporta o frontend (gera os assets estáticos)
RUN reflex init
RUN reflex export --frontend-only --no-zip

EXPOSE 8080

# 2. Roda backend + serve o frontend estático já buildado
CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--backend-port", "8080"]