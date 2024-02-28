from faststream.rabbit import RabbitRouter

from src.api.amqp.v1.users import users_v1
from src.api.amqp.v1.resources import resources_v1
from src.api.amqp.v1.scopes import scopes_v1


api_router = RabbitRouter()

api_router.include_router(users_v1)
api_router.include_router(resources_v1)
api_router.include_router(scopes_v1)
