import os
import urllib
from logging.config import fileConfig

from alembic import context
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from sqlalchemy import engine_from_config, pool

SECRET_NAME = "database-password"


def get_secret_from_vault(vault_url: str) -> str:
    """Recupera el secreto usando la identidad actual (CLI, Service Principal o MSI)"""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(SECRET_NAME).value
    db_password = urllib.parse.quote_plus(secret)
    return db_password


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Obtener configuración del alembic.ini
    connectable_config = context.config.get_section(context.config.config_ini_section)

    # Construir la URL final dinámicamente
    # Supongamos que en alembic.ini solo tienes la base: mssql+pyodbc://usuario:
    base_url = connectable_config.get("sqlalchemy.url")
    vault_url = os.getenv("VAULT_URL") or "https://myvault.vault.azure.net/"
    server_name = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = get_secret_from_vault(vault_url)
    full_url = f"{base_url}{user}:{password}@{server_name}/{database}?driver=ODBC+Driver+18+for+SQL+Server"  # noqa: E501

    connectable = engine_from_config(
        {"sqlalchemy.url": full_url},  # Inyectamos la URL completa aquí
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
