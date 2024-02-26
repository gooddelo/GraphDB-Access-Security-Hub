import uuid

import pytest

from src.entities.user.models import User
from src.entities.user.exceptions import UserAlreadyExistException


@pytest.mark.asyncio
class TestUserModel:
    async def test_create_new_user(self):
        user = User(
            id_=str(uuid.uuid4()),
            attr="user",
        )
        await user.create()
        assert (
            await User.find_one({"id_": user.id_, "attr": "user"}) is not None
        )

    async def test_create_existing_user(self, caplog):
        user = User(
            id_=str(uuid.uuid4()),
            attr="user",
        )
        await user.create()
        with pytest.raises(UserAlreadyExistException, match=f"User {user.id_} with role {user.role} already exists"):
            user_copy = User(
                id_=user.id_,
                attr=user.role,
            )
            await user_copy.create()
