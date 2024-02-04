import uuid

import pytest

from src.entities.namespace.models import Namespace
from src.entities.namespace.dto import NamespaceCreateDTO
from src.entities.namespace.dal import NamespaceDAO


@pytest.mark.asyncio
class TestNamespaceDAL:
    async def test_create_no_relationship(self, neo4j_client):
        data = NamespaceCreateDTO(
            namespace_id=uuid.uuid4(),
            name="company",
            user_ids=[],
            namespace_ids=[],
        )
        await NamespaceDAO.create(neo4j_client, data)
        namespaces = await Namespace.count()
        assert namespaces == 1

    # async def test_read(self, neo4j_client):
    #     pass

    # async def test_update(self, neo4j_client):
    #     pass

    # async def test_delete(self, neo4j_client):
    #     pass
