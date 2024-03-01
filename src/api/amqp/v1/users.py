from faststream.rabbit import RabbitRouter

from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import UserQueuesV1
from src.entities.user.services import UserService
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO
from src.entities.user.dto import UserCreateDTO, UserUpdateDTO, UserPropertiesDTO


users_v1 = RabbitRouter()


@users_v1.subscriber(queue=UserQueuesV1.CREATE, exchange=GASH_EXCHANGE)
async def create_user(data: UserCreateDTO[ScopePropertiesDTO, ResourcePropertiesDTO]):
    await UserService.create(data)


@users_v1.subscriber(queue=UserQueuesV1.UPDATE, exchange=GASH_EXCHANGE)
async def update_user(data: UserUpdateDTO[ScopePropertiesDTO, ResourcePropertiesDTO]):
    await UserService.update(data)


@users_v1.subscriber(queue=UserQueuesV1.DELETE, exchange=GASH_EXCHANGE)
async def delete_user(data: UserPropertiesDTO):
    await UserService.delete(data)
