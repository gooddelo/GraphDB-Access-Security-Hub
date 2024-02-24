from faststream.rabbit import RabbitExchange
from faststream.rabbit.shared.utils import build_url
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class AMQPConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="RABBITMQ_")

    host: str = "localhost"
    port: int = 5672
    default_user: str = "guest"
    default_pass: str = "guest"
    vhost: str = "/"

    def connection_url(self) -> URL:
        return build_url(
            host=self.host,
            port=self.port,
            login=self.default_user,
            password=self.default_pass,
            virtualhost=self.vhost,
        )


AMQP_CONFIG = AMQPConfig()  # type: ignore
GASH_EXCHANGE = RabbitExchange("GASH", auto_delete=True)
