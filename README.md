# core-bff
Core Backend For Frontend (BFF) del tablero. Es el punto de contacto con el frontend.

##  Pre-commit

Asegúrate de estar dentro del entorno de poetry

`poetry run pre-commit install`

Check

`poetry run pre-commit run --all-files`

## Run Tests

`poetry run pytest -v`


## Run app with `Poetry`

`poetry run uvicorn app.main:app --reload`

## Run app with `Colima`

`brew install docker`

`brew install colima`

`colima start`

`docker build . -t eltablero-core-bff:latest`

`docker run -it -p 8000:8000 eltablero-core-bff:latest`


## Basic Tests

### Health

Request:

```sh
curl -i http://localhost:8000/health
```

Response:
```json
{"status":"ok"}
```

### Items

Request:

```sh
curl -i \
  -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{
        "id": 1,
        "name": "Componente Frontend",
        "description": "Un plugin para React",
        "price": 25.5
      }'
```

Response:
```json
{
    "id":1,
    "name":"Componente Frontend",
    "description":"Un plugin para React",
    "price":25.5
}
```
