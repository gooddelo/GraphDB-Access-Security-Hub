from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.api.amqp import api_router
from src.config.amqp import AMQP_CONFIG

broker = RabbitBroker(AMQP_CONFIG.connection_url())
app = FastStream(broker)
broker.include_routers(api_router)

@app.on_startup
async def on_startup():
    broker.include_routers(api_router)
    await broker.connect()
    yield
    await broker.close()
