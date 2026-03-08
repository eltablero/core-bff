import os
import urllib.parse
from functools import cached_property

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    vault_url: str
    secret_name: str = "database-password"
    db_server: str
    db_user: str
    db_name: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @cached_property
    def db_url(self) -> str:
        # Detección de entorno de test
        if os.getenv("PYTEST_CURRENT_TEST"):
            return "mssql+aioodbc://user:pass@localhost/db?driver=ODBC+Driver+18+for+SQL+Server"

        try:
            credential = DefaultAzureCredential()
            client = SecretClient(vault_url=self.vault_url, credential=credential)

            raw_password = client.get_secret(self.secret_name).value or ""
            safe_password = urllib.parse.quote_plus(raw_password)

            driver = "ODBC+Driver+18+for+SQL+Server"
            return (
                f"mssql+aioodbc://{self.db_user}:{safe_password}@"
                f"{self.db_server}:1433/{self.db_name}?"
                f"driver={driver}&Encrypt=yes&TrustServerCertificate=yes"
            )
        except Exception as e:
            raise RuntimeError(f"Fallo crítico al recuperar secreto: {e}")


# Instancia global única
settings = Settings()
