# core-bff
Core Backend For Frontend (BFF) del tablero. Es el punto de contacto con el frontend.

##  Pre-commit

Asegúrate de estar dentro del entorno de poetry

`poetry run pre-commit install`

Check

`poetry run pre-commit run --all-files`

## Run Tests

`poetry run pytest -v`


## Run app

`poetry run uvicorn app.main:app --reload`
