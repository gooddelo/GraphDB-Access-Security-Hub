from faststream.rabbit import RabbitRouter

from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import ScopeQueuesV1
from src.entities.scope.dto import ScopeCreateDTO, ScopeUpdateDTO, ScopePropertiesDTO
from src.entities.scope.services import ScopeService
from src.entities.user.dto import UserPropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


scopes_v1 = RabbitRouter()


@scopes_v1.subscriber(queue=ScopeQueuesV1.CREATE, exchange=GASH_EXCHANGE)
async def create_scope(data: ScopeCreateDTO[UserPropertiesDTO, ResourcePropertiesDTO]):
    await ScopeService.create(data)


@scopes_v1.subscriber(queue=ScopeQueuesV1.UPDATE, exchange=GASH_EXCHANGE)
async def update_scope(data: ScopeUpdateDTO[UserPropertiesDTO, ResourcePropertiesDTO]):
    await ScopeService.update(data)


@scopes_v1.subscriber(queue=ScopeQueuesV1.DELETE, exchange=GASH_EXCHANGE)
async def delete_scope(data: ScopePropertiesDTO):
    await ScopeService.delete(data)
