from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.parent / ".env", env_file_encoding="utf-8")
    print(Path(__file__).parent.parent.parent / ".env")

    API_PORT: int = Field(..., description="API port")
    PYTHONPATH: str = Field(..., description="Python path")
    DB_USER: str = Field(..., description="Database user")
    DB_PASSWORD: str = Field(..., description="Database password")
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(5432, description="Database port")
    DB_NAME: str = Field(..., description="Database name")
    DATABASE_URL: str = Field(..., description="Database URL")

    REDIS_HOST: str = Field(..., description="Redis host")
    REDIS_PORT: int = Field(6379, description="Redis port")

settings = Settings()
