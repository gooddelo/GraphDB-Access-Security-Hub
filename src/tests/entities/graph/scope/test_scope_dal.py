import uuid

import pytest

from src.entities.scope.models import Scope
from src.entities.scope.dto import ScopeCreateDTO, ScopePropertiesDTO, ScopeUpdateDTO
from src.entities.scope.dal import ScopeDAO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


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
        owner = UserPropertiesDTO.model_validate(user_nodes.pop())
        users = [UserPropertiesDTO.model_validate(user) for user in user_nodes]
        scopes = [ScopePropertiesDTO.model_validate(scope) for scope in scope_nodes]
        resources = [
            ResourcePropertiesDTO.model_validate(resource)
            for resource in resource_nodes
        ]

        data = ScopeCreateDTO[UserPropertiesDTO, ResourcePropertiesDTO](
            id_=str(uuid.uuid4()),
            name="company",
            owner=owner,
            users=users,
            scopes=scopes,
            resources=resources,
        )
        await ScopeDAO.create(data)
        scopes_count = await Scope.count()
        scope = await Scope.find_one({"id_": data.id_, "attr": data.name})
        connected_owners = await scope.owner.find_connected_nodes()
        assert len(connected_owners) == 1
        assert scopes_count == 1 + len(scopes)

        connected_users = await scope.users.find_connected_nodes()
        connected_scopes = await scope.scopes.find_connected_nodes()
        connected_resources = await scope.resources.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_scopes) == len(scopes)
        assert len(connected_resources) == len(resources)

    @pytest.mark.parametrize("scope_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_update_name(self, scope_nodes):
        scope = scope_nodes[0]
        new_data = ScopeUpdateDTO[UserPropertiesDTO, ResourcePropertiesDTO](
            id_=scope.id_, old_name=scope.name, new_name="name"
        )
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
            id_=scope.id_,
            old_name=scope.name,
            new_owner=UserPropertiesDTO.model_validate(user_nodes[1]),
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
            id_=scope.id_,
            old_name=scope.name,
            new_users=[UserPropertiesDTO.model_validate(user) for user in new_users],
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
            id_=scope.id_,
            old_name=scope.name,
            new_resources=[ResourcePropertiesDTO.model_validate(resource) for resource in new_resources],
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
        new_data = ScopeUpdateDTO[UserPropertiesDTO, ResourcePropertiesDTO](
            id_=main_scope.id_,
            old_name=main_scope.name,
            new_scopes=[ScopePropertiesDTO.model_validate(scope) for scope in new_scopes],
        )
        await ScopeDAO.update(new_data)
        connected_scopes = await main_scope.scopes.find_connected_nodes()
        assert set(connected_scopes) == set(new_scopes)

    @pytest.mark.parametrize("scope_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_delete(self, scope_nodes):
        scope = scope_nodes[0]
        await ScopeDAO.delete(ScopePropertiesDTO.model_validate(scope))
        assert await Scope.find_one({"id_": scope.id_, "attr": scope.name}) is None
