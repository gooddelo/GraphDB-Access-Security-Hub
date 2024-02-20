from faststream.rabbit import RabbitRouter

from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import UserQueuesV1
from src.entities.user.dto import UserCreateDTO

users_v1 = RabbitRouter()


@users_v1.subscriber(queue=UserQueuesV1.CREATE, exchange=GASH_EXCHANGE)
async def create_user(data: UserCreateDTO):
    return 2
