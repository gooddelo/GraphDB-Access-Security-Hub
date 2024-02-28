from faststream.rabbit import RabbitRouter

from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import ResourceQueuesV1
from src.entities.resource.dto import ResourceCreateDTO, ResourceUpdateDTO, ResourcePropertiesDTO
from src.entities.resource.services import ResourceService


resources_v1 = RabbitRouter()


@resources_v1.subscriber(queue=ResourceQueuesV1.CREATE, exchange=GASH_EXCHANGE)
async def create_resource(data: ResourceCreateDTO):
    await ResourceService.create(data)

@resources_v1.subscriber(queue=ResourceQueuesV1.UPDATE, exchange=GASH_EXCHANGE)
async def update_resource(data: ResourceUpdateDTO):
    await ResourceService.update(data)

@resources_v1.subscriber(queue=ResourceQueuesV1.DELETE, exchange=GASH_EXCHANGE)
async def delete_resource(data: ResourcePropertiesDTO):
    await ResourceService.delete(data)