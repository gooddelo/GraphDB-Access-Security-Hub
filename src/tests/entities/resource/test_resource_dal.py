import uuid

import pytest

from src.entities.resource.models import Resource
from src.entities.resource.dto import ResourceCreateDTO
from src.entities.resource.dal import ResourceDAO


@pytest.mark.asyncio
class TestResourceDAL:
    @pytest.mark.parametrize(
        "user_nodes,namespace_nodes",
        (
            ([], []),
            ([], [uuid.uuid4()]),
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_create(
        self,
        user_nodes,
        namespace_nodes,
    ):
        data = ResourceCreateDTO(
            resource_id=uuid.uuid4(),
            type="resource",
            user_ids=[user.user_id for user in user_nodes],
            namespace_ids=[namespace.namespace_id for namespace in namespace_nodes],
        )
        await ResourceDAO.create(data)
        resources = await Resource.count()
        resource = await Resource.find_one({"resource_id": str(data.resource_id)})
        assert resources == 1

        connected_users = await resource.users.find_connected_nodes()
        connected_namespaces = await resource.namespaces.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_namespaces) == len(namespace_nodes)

    # async def test_read(self, neo4j_client):
    #     pass

    # async def test_update(self, neo4j_client):
    #     pass

    # async def test_delete(self, neo4j_client):
    #     pass
