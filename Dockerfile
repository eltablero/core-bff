# Etapa 1: Constructor (Builder)
FROM python:3.13-slim as builder

# Dependencias para compilar drivers C (pyodbc/aioodbc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==2.3.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# IMPORTANTE: Asegúrate de que 'aioodbc' esté en tu pyproject.toml
RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR

# Etapa 2: Ejecución (Runtime)
FROM python:3.13-slim as runtime

# Instalación del Driver de Microsoft (Capa de sistema)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg2 \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
    msodbcsql18 \
    unixodbc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Configuración de entorno
WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# Copia de artefactos
COPY --from=builder /app/.venv /app/.venv
COPY /src/app/ /app/app/

EXPOSE 8000

# Usuario no-root (Mejora de seguridad para Azure Container Apps)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
