import uuid

import pytest

from src.entities.user.models import User


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
        with pytest.raises(ValueError, match=f"User {user.id_} with attr {user.role} already exists"):
            user_copy = User(
                id_=user.id_,
                attr=user.role,
            )
            await user_copy.create()
