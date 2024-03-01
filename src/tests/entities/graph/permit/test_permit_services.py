import uuid

import pytest
import pytest_asyncio

from src.entities.permit.services import PermitService
from src.entities.permit.dto import PermitRequestDTO
from src.entities.policy.dal import PolicyDAO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


@pytest.mark.asyncio
class TestPermitServices:
    @pytest_asyncio.fixture(autouse=True)
    async def set_policy(self, patch_open_big_policy):
        await PolicyDAO.load()
        yield
        PolicyDAO.policy = {}

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit(self, user_nodes, scope_nodes, resource_nodes):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(owner),
            object=ResourcePropertiesDTO.model_validate(company_resource),
            action="read",
        )
        permit = await PermitService.get_permit(data)
        assert permit is True

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_on_scope(self, user_nodes, scope_nodes, resource_nodes):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(owner),
            object=ScopePropertiesDTO.model_validate(company),
            action="read",
        )
        permit = await PermitService.get_permit(data)
        assert permit is True

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_on_user(self, user_nodes, scope_nodes, resource_nodes):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(owner),
            object=UserPropertiesDTO.model_validate(employee),
            action="delete",
        )
        permit = await PermitService.get_permit(data)
        assert permit is True

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling_point_resource"),
                    (uuid.uuid4(), "personal_resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_limited_depth(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(employee),
            object=ResourcePropertiesDTO.model_validate(personal_resource),
            action="update",
        )
        permit = await PermitService.get_permit(data)
        assert permit is True

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_unauthorized_user(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(employee),
            object=ScopePropertiesDTO.model_validate(company),
            action="read",
        )
        permit = await PermitService.get_permit(data)
        assert permit is False

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_subject_not_found(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO(id_=str(uuid.uuid4()), role="owner"),
            object=ScopePropertiesDTO.model_validate(company),
            action="read",
        )
        permit = await PermitService.get_permit(data)
        assert permit is False

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_role_not_configured(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO(id_=str(uuid.uuid4()), role="not_exist"),
            object=ScopePropertiesDTO.model_validate(company),
            action="read",
        )
        permit = await PermitService.get_permit(data)
        assert permit is False

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_object_not_found(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(owner),
            object=ResourcePropertiesDTO(
                id_=str(uuid.uuid4()), type="company_resource"
            ),
            action="read",
        )
        permit = await PermitService.get_permit(data)
        assert permit is False

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_object_not_configured(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(owner),
            object=ResourcePropertiesDTO(id_=str(uuid.uuid4()), type="not_exist"),
            action="read",
        )
        permit = await PermitService.get_permit(data)
        assert permit is False

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [
                    (uuid.uuid4(), "company_resource"),
                    (uuid.uuid4(), "selling point resource"),
                    (uuid.uuid4(), "personal resource"),
                ],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit_action_not_configured(
        self, user_nodes, scope_nodes, resource_nodes
    ):
        owner, employee = user_nodes
        company, selling_point = scope_nodes
        company_resource, selling_point_resource, personal_resource = resource_nodes
        await company.owner.connect(owner)
        await company.scopes.connect(selling_point)
        await company.resources.connect(company_resource)
        await selling_point.resources.connect(selling_point_resource)
        await selling_point.users.connect(employee)
        await employee.own_scopes.connect(selling_point)
        await employee.resources.connect(personal_resource)
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(owner),
            object=ScopePropertiesDTO.model_validate(company),
            action="not_exist",
        )
        permit = await PermitService.get_permit(data)
        assert permit is False

    @pytest.mark.parametrize(
        "user_nodes",
        ([(uuid.uuid4(), "owner")],),
        indirect=True,
    )
    async def test_get_permit_self(self, user_nodes):
        owner = user_nodes[0]
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.model_validate(owner),
            object=UserPropertiesDTO.model_validate(owner),
            action="create_company",
        )
        permit = await PermitService.get_permit(data)
        assert permit is True
