from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    # Database settings
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/todo_app"
    DB_ECHO: bool = False  # Set to True to log SQL queries

    # JWT settings
    JWT_SECRET: str = "your-super-secret-jwt-key-here-32-characters-minimum"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30

    # Property methods to maintain backward compatibility
    @property
    def database_url(self):
        return self.DATABASE_URL

    @property
    def db_echo(self):
        return self.DB_ECHO

    @property
    def jwt_secret(self):
        return self.JWT_SECRET

    @property
    def jwt_algorithm(self):
        return self.JWT_ALGORITHM

    @property
    def jwt_expiration_minutes(self):
        return self.JWT_EXPIRATION_MINUTES


settings = Settings()