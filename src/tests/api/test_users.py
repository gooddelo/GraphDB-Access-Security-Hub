import uuid

import pytest
from faststream.rabbit import TestRabbitBroker

from src.entities.user.dto import UserCreateDTO
from src.api.amqp.main import broker
from src.api.amqp.v1.queues import UserQueuesV1
from src.config.amqp import GASH_EXCHANGE


@pytest.mark.asyncio
class TestUserAPI:
    async def test_create_user(self):
        user_data = UserCreateDTO(
            user_id=uuid.uuid4(),
            role="owner",
            resource_ids=[],
            belong_scope_ids=[],
        )
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=user_data,
                queue=UserQueuesV1.CREATE,
                exchange=GASH_EXCHANGE,
                rpc=True,
            )
        assert result