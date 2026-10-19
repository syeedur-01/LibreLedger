from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    database_url: SecretStr
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
