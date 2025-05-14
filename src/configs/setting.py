from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    debug: bool = True

    app_host: str = "0.0.0.0"
    app_port: int = 6699

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "jobmanagement"
    db_user: str = "jobuser"
    db_password: str = "jobpassword"
    db_schema: str = "job-management"


@lru_cache
def get_settings():
    return Settings()
