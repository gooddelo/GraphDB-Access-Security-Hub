from pydantic_settings import BaseSettings, SettingsConfigDict


class Neo4jConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NEO4J_")

    driver: str
    host: str
    port: int
    user: str
    password: str
    db: str

    @property
    def connection_string(self) -> str:
        return f"{self.driver}://{self.host}:{self.port}/"


NEO4J_CONFIG = Neo4jConfig()  # type: ignore
