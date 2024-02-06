import uuid
from typing import List

import pytest

from src.entities.user.models import User
from src.entities.namespace.models import Namespace
from src.entities.resource.models import Resource
from src.entities.namespace.dto import NamespaceCreateDTO
from src.entities.namespace.dal import NamespaceDAO


async def create_user_nodes(user_ids: List[uuid.UUID]):
    users = [await User(user_id=user_id, role="user").create() for user_id in user_ids]
    return users


async def create_namespace_nodes(namespace_ids: List[uuid.UUID]):
    namespaces = [
        await Namespace(namespace_id=namespace_id, name="company").create()
        for namespace_id in namespace_ids
    ]
    return namespaces


async def create_resource_nodes(resource_ids: List[uuid.UUID]):
    resources = [
        await Resource(resource_id=resource_id, type="resource").create()
        for resource_id in resource_ids
    ]
    return resources


@pytest.mark.asyncio
class TestNamespaceDAL:
    @pytest.mark.parametrize(
        "user_ids,namespace_ids,resource_ids,"
        "connected_users_number,connected_namespaces_number,connected_resources_number",
        (
            ([], [], [], 0, 0, 0),
            ([uuid.uuid4()], [uuid.uuid4()], [], 1, 1, 0),
            ([uuid.uuid4()], [], [uuid.uuid4()], 1, 0, 1),
            ([], [uuid.uuid4()], [uuid.uuid4()], 0, 1, 1),
            ([uuid.uuid4()], [uuid.uuid4()], [uuid.uuid4()], 1, 1, 1),
        ),
    )
    async def test_create(
        self,
        user_ids,
        namespace_ids,
        resource_ids,
        connected_users_number,
        connected_namespaces_number,
        connected_resources_number,
    ):
        owner = (await create_user_nodes([uuid.uuid4()]))[0]
        await create_user_nodes(user_ids)
        await create_namespace_nodes(namespace_ids)
        await create_resource_nodes(resource_ids)

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
        assert namespaces == 1 + connected_namespaces_number

        connected_users = await namespace.users.find_connected_nodes()
        connected_namespaces = await namespace.namespaces.find_connected_nodes()
        connected_resources = await namespace.resources.find_connected_nodes()
        assert len(connected_users) == connected_users_number
        assert len(connected_namespaces) == connected_namespaces_number
        assert len(connected_resources) == connected_resources_number

        await owner.delete()

    # async def test_read(self, neo4j_client):
    #     pass

    # async def test_update(self, neo4j_client):
    #     pass

    # async def test_delete(self, neo4j_client):
    #     pass
