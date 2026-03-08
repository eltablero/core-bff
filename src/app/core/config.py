import urllib.parse

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Variables que vienen del entorno de Azure Container Apps
    vault_url: str
    secret_name: str = "database-password"
    db_server: str
    db_user: str
    db_name: str

    def get_db_url(self) -> str:
        # Recuperamos la contraseña
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=self.vault_url, credential=credential)

        # Operación síncrona solo al inicio
        raw_password = client.get_secret(self.secret_name).value or ""
        safe_password = urllib.parse.quote_plus(raw_password)

        driver = "ODBC+Driver+18+for+SQL+Server"
        return (
            f"mssql+aioodbc://{self.db_user}:{safe_password}@"
            f"{self.db_server}:1433/{self.db_name}?"
            f"driver={driver}&Encrypt=yes&TrustServerCertificate=yes"
        )


# Instanciamos los settings
settings = Settings()
# Generamos la URL una vez
DATABASE_URL = settings.get_db_url()
