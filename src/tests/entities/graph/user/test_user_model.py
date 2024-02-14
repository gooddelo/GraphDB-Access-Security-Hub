import uuid

import pytest

from src.entities.user.models import User


@pytest.mark.asyncio
class TestUserModel:
    async def test_create_new_user(self):
        user = User(
            user_id=uuid.uuid4(),
            role="user",
        )
        await user.create()
        assert (
            await User.find_one({"user_id": str(user.user_id), "role": "user"}) is not None
        )

    async def test_create_existing_user(self, caplog):
        user = User(
            user_id=uuid.uuid4(),
            role="user",
        )
        await user.create()
        with pytest.raises(ValueError, match=f"User {user.user_id} with role {user.role} already exists"):
            user_copy = User(
                user_id=user.user_id,
                role=user.role,
            )
            await user_copy.create()
