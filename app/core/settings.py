from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    postgres_host: str  # имя сервиса из docker-compose.yml
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    @property
    def postgres_url(self) -> str:
        """
        Build PostgreSQL connection URL.

        :return: Database connection string
        """
        return (
            f"postgresql+psycopg2://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore
