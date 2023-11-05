import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

SHARED_DIR = BASE_DIR.resolve().joinpath("shared")
SHARED_DIR.joinpath("logs").mkdir(exist_ok=True)
DIR_LOGS = SHARED_DIR.joinpath("logs")


class Settings(BaseSettings):
    """Application settings."""

    DB_HOST: str = "db_host"
    USE_DATABASE: str = "mysql"
    DB_ECHO: bool = False

    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: str = "sqlalchemy_study"
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "postgrespwd"

    MYSQL_DB_PORT: int = 3307
    MYSQL_DATABASE: str = "sqlalchemy_study"
    MYSQL_USER: str = "user"
    MYSQL_PASSWORD: str = "mysqlpwd"
    MYSQL_ROOT_PASSWORD: str = "mysqlpwd"

    @property
    def async_db_url(self) -> str:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        async_postgres_url = (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB}"
        )

        async_mysql_url = (
            f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.DB_HOST}:{self.MYSQL_DB_PORT}/{self.MYSQL_DATABASE}"
        )
        if os.environ.get("USE_DATABASE", self.USE_DATABASE).lower() == "postgres":
            return async_postgres_url
        return async_mysql_url

    @property
    def sync_db_url(self) -> str:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        sync_postgres_url = (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB}"
        )

        sync_mysql_url = (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.DB_HOST}:{self.MYSQL_DB_PORT}/{self.MYSQL_DATABASE}"
        )
        if os.environ.get("USE_DATABASE", self.USE_DATABASE).lower() == "postgres":
            return sync_postgres_url
        return sync_mysql_url

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"
