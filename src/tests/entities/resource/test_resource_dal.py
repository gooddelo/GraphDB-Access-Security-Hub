import uuid

import pytest

from src.entities.resource.dto import ResourceCreateDTO
from src.entities.resource.dal import ResourceDAO


@pytest.mark.asyncio
class TestResourceDAL:
    async def test_create_no_relationship(self, neo4j_client):
        data = ResourceCreateDTO(
            resource_id=uuid.uuid4(),
            type="resource",
            user_ids=[],
            namespace_ids=[],
        )
        await ResourceDAO.create(neo4j_client, data)

    async def test_read(self, neo4j_client):
        pass

    async def test_update(self, neo4j_client):
        pass

    async def test_delete(self, neo4j_client):
        pass
