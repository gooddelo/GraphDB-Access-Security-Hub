import uuid

import pytest
import pytest_asyncio
from faststream.rabbit import TestRabbitBroker

from src.api.amqp.main import broker
from src.config.amqp import GASH_EXCHANGE
from src.api.amqp.v1.queues import PermitQueuesV1
from src.entities.policy.dal import PolicyDAO


@pytest.mark.asyncio
class TestPermitAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def set_policy(self, patch_open_big_policy):
        await PolicyDAO.load()
        yield
        PolicyDAO.policy = {}

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit(self, user_nodes, scope_nodes, resource_nodes):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = {
            "subject": {
                "id_": owner.id_,
                "role": owner.role,
            },
            "object": {
                "id_": company_resource.id_,
                "type": company_resource.type,
            },
            "action": "read",
        }
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=data,
                queue=PermitQueuesV1.GET,
                exchange=GASH_EXCHANGE,
                rpc=True,
            )
        assert result is True
