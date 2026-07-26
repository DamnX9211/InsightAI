from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration.
       Every variable defined here will be automatically loaded from the .env file.
    """
    DATABASE_URL: str
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()        