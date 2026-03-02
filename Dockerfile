# Etapa 1: Constructor (Builder)
FROM python:3.13-slim as builder

RUN pip install poetry==2.3.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
# Instalamos solo dependencias de producción para mantener la imagen ligera
RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR

# Etapa 2: Ejecución (Runtime)
FROM python:3.13-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copiamos solo el entorno virtual y el código desde la etapa anterior
COPY --from=builder /app/.venv /app/.venv
COPY /src/app/ /app/app/

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Ejecutamos con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
