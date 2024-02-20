from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.api.amqp import api_router
from src.config.amqp import AMQP_CONFIG

broker = RabbitBroker(AMQP_CONFIG.connection_url())
app = FastStream(broker)


@app.on_startup
async def on_startup():
    broker.include_routers(api_router)
