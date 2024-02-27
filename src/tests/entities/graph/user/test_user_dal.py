import re
import uuid

import pytest

from src.entities.user.models import User
from src.entities.user.dto import UserCreateDTO, UserPropertiesDTO, UserUpdateDTO
from src.entities.user.dal import UserDAO
from src.entities.resource.dto import ResourcePropertiesDTO, ResourceCreateDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.user.exceptions import UserNotFoundException
from src.entities.permit.exceptions import ObjectTypeError
from src.entities.resource.exceptions import ResourceNotFoundException


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
        scopes = [ScopePropertiesDTO.model_validate(scope) for scope in scope_nodes]
        resources = [
            ResourcePropertiesDTO.model_validate(resource)
            for resource in resource_nodes
        ]
        data = UserCreateDTO[ScopePropertiesDTO, ResourcePropertiesDTO](
            id_=str(uuid.uuid4()),
            role="admin",
            resources=resources,
            belong_scopes=scopes,
        )
        await UserDAO.create(data)
        users = await User.count()
        assert users == 1
        user = await User.find_one({"id_": data.id_, "attr": data.role})
        connected_belong_scopes = await user.belong_scopes.find_connected_nodes()
        connected_own_scopes = await user.own_scopes.find_connected_nodes()
        connected_resources = await user.resources.find_connected_nodes()
        assert len(connected_own_scopes) == len(connected_belong_scopes)
        assert len(connected_belong_scopes) == len(scope_nodes)
        assert len(connected_resources) == len(resource_nodes)

    @pytest.mark.parametrize("user_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_update_role(self, user_nodes):
        for user in user_nodes:
            new_data = UserUpdateDTO[ScopePropertiesDTO, ResourcePropertiesDTO](
                id_=user.id_, old_role=user.role, new_role="owner"
            )
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
        new_data = UserUpdateDTO[ScopePropertiesDTO, ResourcePropertiesDTO](
            id_=user.id_,
            old_role=user.role,
            new_belong_scopes=[
                ScopePropertiesDTO.model_validate(scope) for scope in new_belong_scopes
            ],
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
            id_=user.id_,
            old_role=user.role,
            new_resources=[
                ResourcePropertiesDTO.model_validate(resource)
                for resource in new_resources
            ],
        )
        await UserDAO.update(new_data)
        connected_resources = await user.resources.find_connected_nodes()
        assert set(connected_resources) == set(new_resources)

    @pytest.mark.parametrize("user_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_delete(self, user_nodes):
        user = UserPropertiesDTO.model_validate(user_nodes[0])
        await UserDAO.delete(user)
        assert await User.count() == 0

    async def test_delete_not_exist(self):
        wrong_id = str(uuid.uuid4())
        with pytest.raises(
            UserNotFoundException,
            match=f"User {wrong_id} with role not_exist doesn't exist",
        ):
            await UserDAO.delete(UserPropertiesDTO(id_=wrong_id, role="not_exist"))

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
        user_data = UserPropertiesDTO(id_=owner.id_, role=owner.role)
        resource_data = ResourcePropertiesDTO(
            id_=company_resource.id_, type=company_resource.type
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
        user_data = UserPropertiesDTO(id_=owner.id_, role=owner.role)
        resource_data = ResourcePropertiesDTO(
            id_=personal_resource.id_, type=personal_resource.type
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
        user_data = UserPropertiesDTO(id_=str(uuid.uuid4()), role=owner.role)
        resource_data = ResourcePropertiesDTO(
            id_=company_resource.id_, type=company_resource.type
        )
        with pytest.raises(
            UserNotFoundException,
            match=f"User {user_data.id_} with role {user_data.role} doesn't exist",
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
        user_data = UserPropertiesDTO(id_=owner.id_, role=owner.role)
        resource_data = ResourcePropertiesDTO(
            id_=str(uuid.uuid4()), type=company_resource.type
        )
        with pytest.raises(
            ResourceNotFoundException,
            match=f"Resource {resource_data.id_} with type {resource_data.type} doesn't exist",
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
        user_data = UserPropertiesDTO(id_=owner.id_, role=owner.role)
        resource_data = ResourceCreateDTO[UserPropertiesDTO, ScopePropertiesDTO](
            id_=str(uuid.uuid4()),
            type=company_resource.type,
            scopes=[],
            users=[],
        )
        with pytest.raises(ObjectTypeError, match=re.escape(f"{type(resource_data)}")):
            assert await UserDAO.is_reachable(user_data, resource_data)
