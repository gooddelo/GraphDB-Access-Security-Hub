import uuid

import pytest
from faststream.rabbit import TestRabbitBroker

from src.entities.user.dto import UserCreateDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO
from src.entities.scope.exceptions import ScopeNotFoundException
from src.entities.resource.exceptions import ResourceNotFoundException
from src.entities.user.models import User
from src.api.amqp.main import broker
from src.api.amqp.v1.queues import UserQueuesV1
from src.config.amqp import GASH_EXCHANGE


@pytest.mark.asyncio
class TestUserAPI:
    @pytest.mark.parametrize(
        "scope_nodes,resource_nodes",
        (
            ([], []),
            ([uuid.uuid4()], []),
            ([], [uuid.uuid4()]),
            ([uuid.uuid4()], [uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_create_user(self, scope_nodes, resource_nodes):
        scopes = [
            ScopePropertiesDTO(id_=scope.id_, name=scope.attr) for scope in scope_nodes
        ]
        resources = [
            ResourcePropertiesDTO(id_=resource.id_, type=resource.attr)
            for resource in resource_nodes
        ]
        user_data = UserCreateDTO[ScopePropertiesDTO, ResourcePropertiesDTO](
            id_=str(uuid.uuid4()),
            role="admin",
            resources=resources,
            belong_scopes=scopes,
        )
        async with TestRabbitBroker(broker) as test_brocker:
            result = await test_brocker.publish(
                message=user_data,
                queue=UserQueuesV1.CREATE,
                exchange=GASH_EXCHANGE,
            )
        assert result is None
        user = await User.find_one({"id_": user_data.id_, "attr": user_data.role})
        assert User is not None
        connected_belong_scopes = await user.belong_scopes.find_connected_nodes()
        connected_own_scopes = await user.own_scopes.find_connected_nodes()
        connected_resources = await user.resources.find_connected_nodes()
        assert len(connected_own_scopes) == len(connected_belong_scopes)
        assert len(connected_belong_scopes) == len(scope_nodes)
        assert len(connected_resources) == len(resource_nodes)

    @pytest.mark.parametrize(
        "wrong_scopes,wrong_resources",
        (
            ([ScopePropertiesDTO(id_=str(uuid.uuid4()), name="...")], []),  # type: ignore
            ([], [ResourcePropertiesDTO(id_=str(uuid.uuid4()), type="...")]),  # type: ignore
            (
                [ScopePropertiesDTO(id_=str(uuid.uuid4()), name="...")],  # type: ignore
                [ResourcePropertiesDTO(id_=str(uuid.uuid4()), type="...")],  # type: ignore
            ),
        ),
    )
    async def test_create_user_wrong_links(self, wrong_scopes, wrong_resources):
        user_data = UserCreateDTO[ScopePropertiesDTO, ResourcePropertiesDTO](
            id_=str(uuid.uuid4()),
            role="admin",
            resources=wrong_resources,
            belong_scopes=wrong_scopes,
        )
        if wrong_scopes:
            with pytest.raises(ScopeNotFoundException):
                async with TestRabbitBroker(broker) as test_brocker:
                    await test_brocker.publish(
                        message=user_data,
                        queue=UserQueuesV1.CREATE,
                        exchange=GASH_EXCHANGE,
                    )
        else:
            with pytest.raises(ResourceNotFoundException):
                async with TestRabbitBroker(broker) as test_brocker:
                    await test_brocker.publish(
                        message=user_data,
                        queue=UserQueuesV1.CREATE,
                        exchange=GASH_EXCHANGE,
                    )
