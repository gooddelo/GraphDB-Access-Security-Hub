import uuid

import pytest

from src.entities.user.models import User
from src.entities.user.dto import UserCreateDTO
from src.entities.user.dal import UserDAO


@pytest.mark.asyncio
class TestUserDAL:
    @pytest.mark.parametrize(
        "namespace_nodes,resource_nodes",
        (
            ([], []),
            ([uuid.uuid4()], []),
            ([], [uuid.uuid4()]),
            ([uuid.uuid4()], [uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_create(
        self,
        namespace_nodes,
        resource_nodes,
    ):
        namespace_ids = [namespace.namespace_id for namespace in namespace_nodes]
        resource_ids = [resource.resource_id for resource in resource_nodes]
        data = UserCreateDTO(
            user_id=uuid.uuid4(),
            role="admin",
            resource_ids=resource_ids,
            belong_namespace_ids=namespace_ids,
        )
        await UserDAO.create(data)
        users = await User.count()
        assert users == 1
        user = await User.find_one({"user_id": str(data.user_id)})
        connected_belong_namespaces = await user.belong_namespaces.find_connected_nodes()
        connected_own_namespaces = await user.own_namespaces.find_connected_nodes()
        connected_resources = await user.resources.find_connected_nodes()
        assert len(connected_own_namespaces) == len(connected_belong_namespaces)
        assert len(connected_belong_namespaces) == len(namespace_nodes)
        assert len(connected_resources) == len(resource_nodes)

    # async def test_read(self, neo4j_client):
    #     pass

    # async def test_update(self, neo4j_client):
    #     pass

    # async def test_delete(self, neo4j_client):
    #     pass
