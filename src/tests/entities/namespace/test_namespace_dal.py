import uuid

import pytest

from src.entities.namespace.models import Namespace
from src.entities.namespace.dto import NamespaceCreateDTO, NamespaceReadDTO
from src.entities.namespace.dal import NamespaceDAO


@pytest.mark.asyncio
class TestNamespaceDAL:
    @pytest.mark.parametrize(
        "user_nodes,namespace_nodes,resource_nodes",
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
        namespace_nodes,
        resource_nodes,
    ):
        owner = user_nodes.pop()
        user_ids = [user.user_id for user in user_nodes]
        namespace_ids = [namespace.namespace_id for namespace in namespace_nodes]
        resource_ids = [resource.resource_id for resource in resource_nodes]

        data = NamespaceCreateDTO(
            namespace_id=uuid.uuid4(),
            name="company",
            owner_id=owner.user_id,
            user_ids=user_ids,
            namespace_ids=namespace_ids,
            resource_ids=resource_ids,
        )
        await NamespaceDAO.create(data)
        namespaces = await Namespace.count()
        namespace = await Namespace.find_one({"namespace_id": str(data.namespace_id)})
        connected_owners = await namespace.owner.find_connected_nodes()
        assert len(connected_owners) == 1
        assert namespaces == 1 + len(namespace_ids)

        connected_users = await namespace.users.find_connected_nodes()
        connected_namespaces = await namespace.namespaces.find_connected_nodes()
        connected_resources = await namespace.resources.find_connected_nodes()
        assert len(connected_users) == len(user_nodes)
        assert len(connected_namespaces) == len(namespace_ids)
        assert len(connected_resources) == len(resource_ids)

    @pytest.mark.parametrize("namespace_nodes", ([uuid.uuid4()],), indirect=True)
    async def test_read(self, namespace_nodes):
        namespace_ids = [namespace.namespace_id for namespace in namespace_nodes]
        for namespace_id in namespace_ids:
            namespace_data = await NamespaceDAO.read(namespace_id)
            assert isinstance(namespace_data, NamespaceReadDTO)
            assert namespace_data.namespace_id == namespace_id
            assert namespace_data.name == "company"

    # async def test_update(self):
    #     pass

    # async def test_delete(self):
    #     pass
