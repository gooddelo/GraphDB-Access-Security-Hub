import uuid

import pytest
import pytest_asyncio

from src.entities.permit.services import get_permit
from src.entities.permit.dto import PermitRequestDTO
from src.entities.config.dal import ConfigDAO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


@pytest.mark.asyncio
class TestPermitServices:
    @pytest_asyncio.fixture(autouse=True)
    async def set_config(self, patch_open_big_config):
        await ConfigDAO.load()

    @pytest.mark.parametrize(
        "user_nodes,scope_nodes,resource_nodes",
        (
            (
                [(uuid.uuid4(), "owner"), (uuid.uuid4(), "employee")],
                [(uuid.uuid4(), "company"), (uuid.uuid4(), "selling point")],
                [(uuid.uuid4(), "company_resource"), (uuid.uuid4(), "selling point resource"), (uuid.uuid4(), "personal resource")],
            ),
        ),
        indirect=True,
    )
    async def test_get_permit(self, user_nodes, scope_nodes, resource_nodes):
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
        data = PermitRequestDTO(
            subject=UserPropertiesDTO.from_orm(owner),
            object=ResourcePropertiesDTO.from_orm(company_resource),
            action="read",
        )
        permit = await get_permit(data)
        assert permit is True
