from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.api.amqp import api_router
from src.config.amqp import AMQP_CONFIG
from src.database import init_client
from src.entities.policy.services import init_policy

broker = RabbitBroker(AMQP_CONFIG.connection_url())
app = FastStream(broker)
broker.include_routers(api_router)


@app.on_startup
async def on_startup():
    await init_policy()
    await init_client()
    await broker.connect()


@app.on_shutdown
async def on_shutdown():
    await broker.close()
