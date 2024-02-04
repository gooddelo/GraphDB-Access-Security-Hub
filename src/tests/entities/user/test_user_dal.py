import uuid

import pytest

from src.entities.user.models import User
from src.entities.user.dto import UserCreateDTO
from src.entities.user.dal import UserDAO


@pytest.mark.asyncio
class TestUserDAL:
    async def test_create_no_relationship(self, neo4j_client):
        data = UserCreateDTO(
            user_id=uuid.uuid4(),
            role="admin",
            resource_ids=[],
            belong_namespace_ids=[],
        )
        await UserDAO.create(neo4j_client, data)
        users = await User.count()
        assert users == 1

    # async def test_read(self, neo4j_client):
    #     pass

    # async def test_update(self, neo4j_client):
    #     pass

    # async def test_delete(self, neo4j_client):
    #     pass
