from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    SQLITE_URL: str
    
    SECRET_KEY: str
    
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_PASSWORD: str
    
    
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()