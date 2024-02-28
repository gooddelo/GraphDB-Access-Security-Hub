from faststream.rabbit import RabbitRouter

from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import PermitQueuesV1
from src.entities.permit.dto import PermitRequestDTO
from src.entities.permit.services import PermitService


permit_v1 = RabbitRouter()


@permit_v1.subscriber(queue=PermitQueuesV1.GET, exchange=GASH_EXCHANGE)
async def get_permit(data: PermitRequestDTO):
    return await PermitService.get_permit(data)
