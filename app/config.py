from pydantic_settings import BaseSettings, SettingsConfigDict


class HackathonServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: str

    USER_SERVICE_URL: str
    USER_SERVICE_API_KEY: str

    TEAM_SERVICE_URL: str
    TEAM_SERVICE_API_KEY: str

    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str

    JWT_SECRET: str = "dstu"
    ROOT_PATH: str = "/"
    INTERNAL_API_KEY: str = "apikey"
    PUBLIC_API_URL: str = "http://localhost/hackathon/"


Settings = HackathonServiceSettings()
