from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    MONGODB_URI: str
    MONGODB_DATABASE: str
    TELEGRAM_BOT_TOKEN: str
    GEMINI_API_KEY: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

settings = Settings()

