import uuid

import pytest

from src.entities.resource.models import Resource
from src.entities.resource.dto import (
    ResourceCreateDTO,
    ResourceReadDTO,
    ResourceUpdateDTO,
)
from src.entities.resource.dal import ResourceDAO


@pytest.mark.asyncio
class TestResourceDAL:
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
    async def test_create(
        self,
        user_nodes,
        scope_nodes,
    ):
        data = ResourceCreateDTO(
            resource_id=uuid.uuid4(),
            type="resource",
            user_ids=[user.user_id for user in user_nodes],
            scope_ids=[scope.scope_id for scope in scope_nodes],
        )
        await ResourceDAO.create(data)
        resources = await Resource.count()
        resource = await Resource.find_one({"resource_id": str(data.resource_id)})
        assert resources == 1

        connected_users = await resource.users.find_connected_nodes()
        connected_scopes = await resource.scopes.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_scopes) == len(scope_nodes)

    @pytest.mark.parametrize("resource_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_read(self, resource_nodes):
        resource_ids = [resource.resource_id for resource in resource_nodes]
        for resource_id in resource_ids:
            resource_data = await ResourceDAO.read(resource_id)
            assert isinstance(resource_data, ResourceReadDTO)
            assert resource_data.resource_id == resource_id
            assert resource_data.type == "resource"

    @pytest.mark.parametrize("resource_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_update_type(self, resource_nodes):
        resource = resource_nodes[0]
        new_data = ResourceUpdateDTO(
            resource_id=resource.resource_id,
            new_type="new_type",
        )
        await ResourceDAO.update(new_data)
        await resource.refresh()
        assert resource.type == "new_type"

    @pytest.mark.parametrize(
        "resource_nodes,user_nodes",
        (
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_update_users(self, resource_nodes, user_nodes):
        resource = resource_nodes[0]
        old_users = user_nodes[: len(user_nodes) // 2]
        new_users = user_nodes[len(user_nodes) // 2 :]
        for user in old_users:
            await resource.users.connect(user)
        new_data = ResourceUpdateDTO(
            resource_id=resource.resource_id,
            new_user_ids=[user.user_id for user in new_users],
        )
        await ResourceDAO.update(new_data)
        connected_users = await resource.users.find_connected_nodes()
        assert set(connected_users) == set(new_users)
    
    @pytest.mark.parametrize(
        "resource_nodes,scope_nodes",
        (
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_update_scopes(self, resource_nodes, scope_nodes):
        resource = resource_nodes[0]
        old_scopes = scope_nodes[: len(scope_nodes) // 2]
        new_scopes = scope_nodes[len(scope_nodes) // 2 :]
        for scope in old_scopes:
            await resource.scopes.connect(scope)
        new_data = ResourceUpdateDTO(
            resource_id=resource.resource_id,
            new_scope_ids=[scope.scope_id for scope in new_scopes],
        )
        await ResourceDAO.update(new_data)
        connected_scopes = await resource.scopes.find_connected_nodes()
        assert set(connected_scopes) == set(new_scopes)

    # async def test_delete(self, neo4j_client):
    #     pass
