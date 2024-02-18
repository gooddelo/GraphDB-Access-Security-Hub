import re
import uuid

import pytest

from src.entities.user.models import User
from src.entities.user.dto import UserCreateDTO, UserPropertiesDTO, UserUpdateDTO
from src.entities.user.dal import UserDAO
from src.entities.resource.dto import ResourcePropertiesDTO, ResourceCreateDTO
from src.entities.user.exceptions import (
    UserNotFoundException,
    ObjectNotFoundException,
    ObjectTypeError,
)


@pytest.mark.asyncio
class TestUserDAL:
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
        await UserDAO.create(data)
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
    async def test_read(self, user_nodes):
        user_ids = [user.user_id for user in user_nodes]
        for user_id in user_ids:
            user_data = await UserDAO.read(user_id)
            assert isinstance(user_data, UserPropertiesDTO)
            assert user_data.user_id == user_id
            assert user_data.role == "user"

    @pytest.mark.parametrize("user_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_update_role(self, user_nodes):
        for user in user_nodes:
            new_data = UserUpdateDTO(user_id=user.user_id, new_role="owner")
            await UserDAO.update(new_data)
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
        await UserDAO.update(new_data)
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
        await UserDAO.update(new_data)
        connected_resources = await user.resources.find_connected_nodes()
        assert set(connected_resources) == set(new_resources)

    @pytest.mark.parametrize("user_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_delete(self, user_nodes):
        user = user_nodes[0]
        await UserDAO.delete(user.user_id)
        assert await User.count() == 0

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4()],
            ),
        ),
        indirect=True,
    )
    async def test_is_reachable_with_multihop(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner = user_nodes[0]
        employee = user_nodes[1]
        company = scope_nodes[0]
        selling_point = scope_nodes[1]
        company_resource = resource_nodes[0]
        selling_point_resource = resource_nodes[1]
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        user_data = UserPropertiesDTO(user_id=owner.user_id, role=owner.role)
        resource_data = ResourcePropertiesDTO(
            resource_id=company_resource.resource_id, type=company_resource.type
        )
        assert await UserDAO.is_reachable(user_data, resource_data)

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
            ),
        ),
        indirect=True,
    )
    async def test_is_reachable_with_depth(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner = user_nodes[0]
        employee = user_nodes[1]
        company = scope_nodes[0]
        selling_point = scope_nodes[1]
        company_resource = resource_nodes[0]
        selling_point_resource = resource_nodes[1]
        personal_resource = resource_nodes[2]
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        user_data = UserPropertiesDTO(user_id=owner.user_id, role=owner.role)
        resource_data = ResourcePropertiesDTO(
            resource_id=personal_resource.resource_id, type=personal_resource.type
        )
        assert await UserDAO.is_reachable(user_data, resource_data, 1) is False

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
            ),
        ),
        indirect=True,
    )
    async def test_is_reachable_user_not_exist(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner = user_nodes[0]
        employee = user_nodes[1]
        company = scope_nodes[0]
        selling_point = scope_nodes[1]
        company_resource = resource_nodes[0]
        selling_point_resource = resource_nodes[1]
        personal_resource = resource_nodes[2]
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        user_data = UserPropertiesDTO(user_id=uuid.uuid4(), role=owner.role)
        resource_data = ResourcePropertiesDTO(
            resource_id=company_resource.resource_id, type=company_resource.type
        )
        with pytest.raises(
            UserNotFoundException,
            match=re.escape(f"Subj: {user_data}; Obj: ; Act: ;"),
        ):
            assert await UserDAO.is_reachable(user_data, resource_data)

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
            ),
        ),
        indirect=True,
    )
    async def test_is_reachable_object_not_exist(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner = user_nodes[0]
        employee = user_nodes[1]
        company = scope_nodes[0]
        selling_point = scope_nodes[1]
        company_resource = resource_nodes[0]
        selling_point_resource = resource_nodes[1]
        personal_resource = resource_nodes[2]
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        user_data = UserPropertiesDTO(user_id=owner.user_id, role=owner.role)
        resource_data = ResourcePropertiesDTO(
            resource_id=uuid.uuid4(), type=company_resource.type
        )
        with pytest.raises(
            ObjectNotFoundException,
            match=re.escape(f"Subj: ; Obj: {resource_data}; Act: ;"),
        ):
            assert await UserDAO.is_reachable(user_data, resource_data)

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4()],
                [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()],
            ),
        ),
        indirect=True,
    )
    async def test_is_reachable_object_wrong_dto_type(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner = user_nodes[0]
        employee = user_nodes[1]
        company = scope_nodes[0]
        selling_point = scope_nodes[1]
        company_resource = resource_nodes[0]
        selling_point_resource = resource_nodes[1]
        personal_resource = resource_nodes[2]
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        user_data = UserPropertiesDTO(user_id=owner.user_id, role=owner.role)
        resource_data = ResourceCreateDTO(
            resource_id=uuid.uuid4(),
            type=company_resource.type,
            scope_ids=[],
            user_ids=[],
        )
        with pytest.raises(
            ObjectTypeError, match=re.escape(f"{type(resource_data)}")
        ):
            assert await UserDAO.is_reachable(user_data, resource_data)
