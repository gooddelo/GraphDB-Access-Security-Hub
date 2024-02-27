import uuid

import pytest

from src.entities.user.models import User
from src.entities.scope.models import Scope
from src.entities.resource.models import Resource
from src.entities.resource.dal import ResourceDAO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.exceptions import ResourceNotFoundException
from src.entities.resource.dto import (
    ResourceCreateDTO,
    ResourcePropertiesDTO,
    ResourceUpdateDTO,
)


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
            id_=str(uuid.uuid4()),
            type="resource",
            users=[UserPropertiesDTO.model_validate(user) for user in user_nodes],
            scopes=[ScopePropertiesDTO.model_validate(scope) for scope in scope_nodes],
        )
        await ResourceDAO.create(data)
        resources = await Resource.count()
        resource = await Resource.find_one({"id_": data.id_, "attr": data.type})
        assert resources == 1

        connected_users = await resource.users.find_connected_nodes()
        connected_scopes = await resource.scopes.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_scopes) == len(scope_nodes)

    @pytest.mark.parametrize("resource_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_update_type(self, resource_nodes):
        resource = resource_nodes[0]
        new_data = ResourceUpdateDTO(
            id_=resource.id_,
            old_type=resource.type,
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
        new_data = ResourceUpdateDTO[UserPropertiesDTO, ScopePropertiesDTO](
            id_=resource.id_,
            old_type=resource.type,
            new_users=[UserPropertiesDTO.model_validate(user) for user in new_users],
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
        new_data = ResourceUpdateDTO[UserPropertiesDTO, ScopePropertiesDTO](
            id_=resource.id_,
            old_type=resource.type,
            new_scopes=[ScopePropertiesDTO.model_validate(scope) for scope in new_scopes],
        )
        await ResourceDAO.update(new_data)
        connected_scopes = await resource.scopes.find_connected_nodes()
        assert set(connected_scopes) == set(new_scopes)

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
        await ResourceDAO.delete(ResourcePropertiesDTO.model_validate(resource))
        assert (
            await Resource.find_one(resource.model_dump()) is None
        )
        assert await User.find_one({"id_": user.id_, "attr": user.role}) is not None
        assert await Scope.find_one({"id_": scope.id_, "attr": scope.name}) is not None
        assert len(await user.resources.find_connected_nodes()) == 0
        assert len(await scope.resources.find_connected_nodes()) == 0

    async def test_delete_not_exist(self):
        wrong_id = str(uuid.uuid4())
        with pytest.raises(
            ResourceNotFoundException,
            match=f"Resource {wrong_id} with type not_exist doesn't exist",
        ):
            await ResourceDAO.delete(ResourcePropertiesDTO(id_=wrong_id, type="not_exist"))
