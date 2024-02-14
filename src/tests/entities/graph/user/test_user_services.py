import uuid

import pytest

from src.entities.user.models import User
from src.entities.user.dto import UserCreateDTO, UserUpdateDTO
from src.entities.user.services import UserService


@pytest.mark.asyncio
class TestUserServise:
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
    async def test_create(
        self,
        scope_nodes,
        resource_nodes,
    ):
        scope_ids = [scope.scope_id for scope in scope_nodes]
        resource_ids = [resource.resource_id for resource in resource_nodes]
        data = UserCreateDTO(
            user_id=uuid.uuid4(),
            role="admin",
            resource_ids=resource_ids,
            belong_scope_ids=scope_ids,
        )
        await UserService.create(data)
        users = await User.count()
        assert users == 1
        user = await User.find_one({"user_id": str(data.user_id)})
        connected_belong_scopes = await user.belong_scopes.find_connected_nodes()
        connected_own_scopes = await user.own_scopes.find_connected_nodes()
        connected_resources = await user.resources.find_connected_nodes()
        assert len(connected_own_scopes) == len(connected_belong_scopes)
        assert len(connected_belong_scopes) == len(scope_nodes)
        assert len(connected_resources) == len(resource_nodes)

    @pytest.mark.parametrize("user_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_update_role(self, user_nodes):
        for user in user_nodes:
            new_data = UserUpdateDTO(user_id=user.user_id, new_role="owner")
            await UserService.update(new_data)
            await user.refresh()
            assert user.role == new_data.new_role

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes",
        (
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_update_scopes(self, user_nodes, scope_nodes):
        user = user_nodes[0]
        old_belong_scopes = scope_nodes[: len(scope_nodes) // 2]
        new_belong_scopes = scope_nodes[len(scope_nodes) // 2 :]
        for scope in old_belong_scopes:
            await user.belong_scopes.connect(scope)
            await user.own_scopes.connect(scope)
        new_data = UserUpdateDTO(
            user_id=user.user_id,
            new_belong_scope_ids=[scope.scope_id for scope in new_belong_scopes],
        )
        await UserService.update(new_data)
        connected_belong_scopes = await user.belong_scopes.find_connected_nodes()
        assert set(connected_belong_scopes) == set(new_belong_scopes)

    @pytest.mark.parametrize(
        "user_nodes,resource_nodes",
        (
            ([uuid.uuid4()], []),
            ([uuid.uuid4()], [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]),
        ),
        indirect=True,
    )
    async def test_update_resources(self, user_nodes, resource_nodes):
        user = user_nodes[0]
        old_resources = resource_nodes[: len(resource_nodes) // 2]
        new_resources = resource_nodes[len(resource_nodes) // 2 :]
        for resource in old_resources:
            await user.resources.connect(resource)
        new_data = UserUpdateDTO(
            user_id=user.user_id,
            new_resource_ids=[resource.resource_id for resource in new_resources],
        )
        await UserService.update(new_data)
        connected_resources = await user.resources.find_connected_nodes()
        assert set(connected_resources) == set(new_resources)

    @pytest.mark.parametrize("user_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_delete(self, user_nodes):
        user = user_nodes[0]
        await UserService.delete(user.user_id)
        assert await User.count() == 0