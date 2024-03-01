import uuid

import pytest
from faststream.rabbit import TestRabbitBroker

from src.api.amqp.main import broker
from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import ScopeQueuesV1
from src.entities.scope.models import Scope
from src.entities.scope.dto import ScopeUpdateDTO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


@pytest.mark.asyncio
class TestScopeAPI:
    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            ([uuid.uuid4()], [], []),
            ([uuid.uuid4(), uuid.uuid4()], [uuid.uuid4()], []),
            ([uuid.uuid4(), uuid.uuid4()], [], [uuid.uuid4()]),
            ([uuid.uuid4()], [uuid.uuid4()], [uuid.uuid4()]),
            ([uuid.uuid4(), uuid.uuid4()], [uuid.uuid4()], [uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_create(
        self,
        user_nodes,
        scope_nodes,
        resource_nodes,
    ):
        owner = user_nodes.pop()
        owner = {"id_": owner.id_, "role": owner.role}
        users = [{"id_": user.id_, "role": user.role} for user in user_nodes]
        scopes = [{"id_": scope.id_, "name": scope.name} for scope in scope_nodes]
        resources = [
            {"id_": resource.id_, "type": resource.type} for resource in resource_nodes
        ]
        data = {
            "id_": str(uuid.uuid4()),
            "name": "company",
            "owner": owner,
            "users": users,
            "scopes": scopes,
            "resources": resources,
        }
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=data,
                queue=ScopeQueuesV1.CREATE,
                exchange=GASH_EXCHANGE,
            )
        assert result is None
        scopes_count = await Scope.count()
        scope = await Scope.find_one({"id_": data["id_"], "attr": data["name"]})
        connected_owners = await scope.owner.find_connected_nodes()
        assert len(connected_owners) == 1
        assert scopes_count == 1 + len(scopes)

        connected_users = await scope.users.find_connected_nodes()
        connected_scopes = await scope.scopes.find_connected_nodes()
        connected_resources = await scope.resources.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_scopes) == len(scopes)
        assert len(connected_resources) == len(resources)

    @pytest.mark.parametrize(
        "scope_nodes,user_nodes",
        (
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_update_users(self, scope_nodes, user_nodes):
        scope = scope_nodes[0]
        old_users = user_nodes[: len(user_nodes) // 2]
        new_users = user_nodes[len(user_nodes) // 2 :]
        for user in old_users:
            await scope.users.connect(user)
        new_data = {
            "id_": scope.id_,
            "old_name": scope.name,
            "new_users": [{"id_": user.id_, "role": user.role} for user in new_users],
        }
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=new_data,
                queue=ScopeQueuesV1.UPDATE,
                exchange=GASH_EXCHANGE,
            )
        assert result is None
        connected_users = await scope.users.find_connected_nodes()
        assert set(connected_users) == set(new_users)

    @pytest.mark.parametrize("scope_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_delete(self, scope_nodes):
        scope = scope_nodes[0]
        data = {"id_": scope.id_, "name": scope.attr}
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=data,
                queue=ScopeQueuesV1.DELETE,
                exchange=GASH_EXCHANGE,
            )
        assert result is None
        assert await Scope.find_one({"id_": scope.id_, "attr": scope.name}) is None
