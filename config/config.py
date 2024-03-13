from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    TG_BOT_API_KEY: str
    TG_ADMIN_CHAT_ID: list[str]

    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_USER: str
    DB_PASS: str
    DB_ECHO: bool

    REDIS_PASSWORD: str

    CAT_API_KEY: str

    @property
    def connection_string_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    @property
    def connection_string_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
