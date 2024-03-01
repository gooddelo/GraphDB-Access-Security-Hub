import uuid

import pytest
from faststream.rabbit import TestRabbitBroker

from src.api.amqp.main import broker
from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import ResourceQueuesV1
from src.entities.user.models import User
from src.entities.scope.models import Scope
from src.entities.resource.models import Resource


@pytest.mark.asyncio
class TestResourcesAPI:
    @pytest.mark.parametrize(
        "user_nodes,scope_nodes",
        (
            ([], []),
            ([], [uuid.uuid4()]),
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_create_resource(
        self,
        user_nodes,
        scope_nodes,
    ):
        data = {
            "id_": str(uuid.uuid4()),
            "type": "resource",
            "users": [{"id_": user.id_, "role": user.role} for user in user_nodes],
            "scopes": [{"id_": scope.id_, "name": scope.name} for scope in scope_nodes],
        }
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=data,
                queue=ResourceQueuesV1.CREATE,
                exchange=GASH_EXCHANGE,
            )
        assert result is None
        resources = await Resource.count()
        resource = await Resource.find_one({"id_": data["id_"], "attr": data["type"]})
        assert resources == 1

        connected_users = await resource.users.find_connected_nodes()
        connected_scopes = await resource.scopes.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_scopes) == len(scope_nodes)

    @pytest.mark.parametrize(
        "resource_nodes,user_nodes",
        (
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_update_resource_users(self, resource_nodes, user_nodes):
        resource = resource_nodes[0]
        old_users = user_nodes[: len(user_nodes) // 2]
        new_users = user_nodes[len(user_nodes) // 2 :]
        for user in old_users:
            await resource.users.connect(user)
        new_data = {
            "id_": resource.id_,
            "old_type": resource.type,
            "new_users": [{"id_": user.id_, "role": user.role} for user in new_users],
        }
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=new_data,
                queue=ResourceQueuesV1.UPDATE,
                exchange=GASH_EXCHANGE,
            )
        assert result is None
        connected_users = await resource.users.find_connected_nodes()
        assert set(connected_users) == set(new_users)

    @pytest.mark.parametrize(
        "resource_nodes,user_nodes,scope_nodes",
        (([uuid.uuid4()], [uuid.uuid4()], [uuid.uuid4()]),),
        indirect=True,
    )
    async def test_delete(self, resource_nodes, user_nodes, scope_nodes):
        resource = resource_nodes[0]
        user = user_nodes[0]
        scope = scope_nodes[0]
        await resource.users.connect(user)
        await resource.scopes.connect(scope)
        data = {"id_": resource.id_, "type": resource.type}
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=data,
                queue=ResourceQueuesV1.DELETE,
                exchange=GASH_EXCHANGE,
            )
        assert result is None
        assert await Resource.find_one(resource.model_dump()) is None
        assert await User.find_one({"id_": user.id_, "attr": user.role}) is not None
        assert await Scope.find_one({"id_": scope.id_, "attr": scope.name}) is not None
        assert len(await user.resources.find_connected_nodes()) == 0
        assert len(await scope.resources.find_connected_nodes()) == 0
