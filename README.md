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

Usar este comando para obtener el appId, password, tenant para pruebas locales:

```
az ad sp create-for-rbac --name "sp-eltablero-dev" --role "Key Vault Secrets User" \
  --scopes "/subscriptions/<tu-sub-id>/resourceGroups/<tu-rg>/providers/Microsoft.KeyVault/vaults/eltableroiackv"
```

```
docker run -it -p 8000:8000 --network="host" \
  -e AZURE_CLIENT_ID="<appId>" \
  -e AZURE_CLIENT_SECRET="<password>" \
  -e AZURE_TENANT_ID="<tenant>" \
  -e VAULT_URL="https://eltableroiackv.vault.azure.net/" \
  -e DB_SERVER="<servidor>.database.windows.net" \
  -e DB_NAME="core-db" \
  -e DB_USER="eltableroadmin" \
  eltablero-core-bff:latest
```

Si la infra esta recién creada, utiliza el siguiente comando para ver tu ip y agregarla al firewall del servidor de base de datos:

```
curl ifconfig.me
```


## Basic Tests

### Health

Request:

```sh
curl -i http://localhost:8000/api/v1/liveness
```

Response:
```json
{
  "status":"alive"
}
```

```sh
curl -i http://localhost:8000/api/v1/health
```

Response:
```json
{
  "status":"ok",
  "checks": {}
}
```
