from faststream.rabbit import RabbitRouter

from src.api.amqp.v1.users import users_v1


api_router = RabbitRouter()

api_router.include_router(users_v1)
