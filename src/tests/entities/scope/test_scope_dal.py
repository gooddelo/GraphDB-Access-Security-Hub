import uuid

import pytest

from src.entities.scope.models import Scope
from src.entities.scope.dto import ScopeCreateDTO, ScopeReadDTO, ScopeUpdateDTO
from src.entities.scope.dal import ScopeDAO


@pytest.mark.asyncio
class TestScopeDAL:
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
        user_ids = [user.user_id for user in user_nodes]
        scope_ids = [scope.scope_id for scope in scope_nodes]
        resource_ids = [resource.resource_id for resource in resource_nodes]

        data = ScopeCreateDTO(
            scope_id=uuid.uuid4(),
            name="company",
            owner_id=owner.user_id,
            user_ids=user_ids,
            scope_ids=scope_ids,
            resource_ids=resource_ids,
        )
        await ScopeDAO.create(data)
        scopes = await Scope.count()
        scope = await Scope.find_one({"scope_id": str(data.scope_id)})
        connected_owners = await scope.owner.find_connected_nodes()
        assert len(connected_owners) == 1
        assert scopes == 1 + len(scope_ids)

        connected_users = await scope.users.find_connected_nodes()
        connected_scopes = await scope.scopes.find_connected_nodes()
        connected_resources = await scope.resources.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_scopes) == len(scope_ids)
        assert len(connected_resources) == len(resource_ids)

    @pytest.mark.parametrize("scope_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_read(self, scope_nodes):
        scope_ids = [scope.scope_id for scope in scope_nodes]
        for scope_id in scope_ids:
            scope_data = await ScopeDAO.read(scope_id)
            assert isinstance(scope_data, ScopeReadDTO)
            assert scope_data.scope_id == scope_id
            assert scope_data.name == "company"

    @pytest.mark.parametrize("scope_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_update_name(self, scope_nodes):
        scope = scope_nodes[0]
        new_data = ScopeUpdateDTO(scope_id=scope.scope_id, new_name="name")
        await ScopeDAO.update(new_data)
        await scope.refresh()
        assert scope.name == "name"

    @pytest.mark.parametrize(
        "scope_nodes,user_nodes",
        (([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4()]),),
        indirect=True,
    )
    async def test_update_owner(self, scope_nodes, user_nodes):
        scope = scope_nodes[0]
        await scope.owner.connect(user_nodes[0])
        new_data = ScopeUpdateDTO(
            scope_id=scope.scope_id,
            new_owner_id=user_nodes[1].user_id,
        )
        await ScopeDAO.update(new_data)
        assert await scope.owner.find_connected_nodes() == [user_nodes[1]]

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
        new_data = ScopeUpdateDTO(
            scope_id=scope.scope_id,
            new_user_ids=[user.user_id for user in new_users],
        )
        await ScopeDAO.update(new_data)
        connected_users = await scope.users.find_connected_nodes()
        assert set(connected_users) == set(new_users)

    @pytest.mark.parametrize(
        "scope_nodes,resource_nodes",
        (
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_update_resources(self, scope_nodes, resource_nodes):
        scope = scope_nodes[0]
        old_resources = resource_nodes[: len(resource_nodes) // 2]
        new_resources = resource_nodes[len(resource_nodes) // 2 :]
        for resource in old_resources:
            await scope.resources.connect(resource)
        new_data = ScopeUpdateDTO(
            scope_id=scope.scope_id,
            new_resource_ids=[resource.resource_id for resource in new_resources],
        )
        await ScopeDAO.update(new_data)
        connected_resources = await scope.resources.find_connected_nodes()
        assert set(connected_resources) == set(new_resources)

    @pytest.mark.parametrize(
        "scope_nodes",
        (
            [uuid.uuid4()],
            [uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
        ),
        indirect=True,
    )
    async def test_update_scopes(self, scope_nodes):
        main_scope = scope_nodes.pop()
        old_scopes = scope_nodes[: len(scope_nodes) // 2]
        new_scopes = scope_nodes[len(scope_nodes) // 2 :]
        for scope in old_scopes:
            await main_scope.scopes.connect(scope)
        new_data = ScopeUpdateDTO(
            scope_id=main_scope.scope_id,
            new_scope_ids=[scope.scope_id for scope in new_scopes],
        )
        await ScopeDAO.update(new_data)
        connected_scopes = await main_scope.scopes.find_connected_nodes()
        assert set(connected_scopes) == set(new_scopes)

    # async def test_delete(self):
    #     pass
