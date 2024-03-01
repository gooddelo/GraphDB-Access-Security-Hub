from faststream.rabbit import RabbitRouter

from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import ResourceQueuesV1
from src.entities.resource.dto import (
    ResourceCreateDTO,
    ResourceUpdateDTO,
    ResourcePropertiesDTO,
)
from src.entities.resource.services import ResourceService
from src.entities.user.dto import UserPropertiesDTO
from src.entities.scope.dto import ScopePropertiesDTO

resources_v1 = RabbitRouter()


@resources_v1.subscriber(queue=ResourceQueuesV1.CREATE, exchange=GASH_EXCHANGE)
async def create_resource(
    data: ResourceCreateDTO[UserPropertiesDTO, ScopePropertiesDTO],
):
    await ResourceService.create(data)


@resources_v1.subscriber(queue=ResourceQueuesV1.UPDATE, exchange=GASH_EXCHANGE)
async def update_resource(
    data: ResourceUpdateDTO[UserPropertiesDTO, ScopePropertiesDTO],
):
    await ResourceService.update(data)


@resources_v1.subscriber(queue=ResourceQueuesV1.DELETE, exchange=GASH_EXCHANGE)
async def delete_resource(data: ResourcePropertiesDTO):
    await ResourceService.delete(data)
