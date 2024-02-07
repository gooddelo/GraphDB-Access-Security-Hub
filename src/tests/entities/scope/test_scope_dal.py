import uuid

import pytest

from src.entities.scope.models import Scope
from src.entities.scope.dto import ScopeCreateDTO, ScopeReadDTO
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

    # async def test_update(self):
    #     pass

    # async def test_delete(self):
    #     pass
