import uuid

from src.entities.user.dal import UserDAO
from src.entities.user.dto import UserCreateDTO, UserUpdateDTO


class UserService:
    dao = UserDAO

    @classmethod
    async def create(cls, user_data: UserCreateDTO):
        return await cls.dao.create(user_data)

    @classmethod
    async def update(cls, user_data: UserUpdateDTO):
        return await cls.dao.update(user_data)

    @classmethod
    async def delete(cls, user_id: uuid.UUID):
        return await cls.dao.delete(user_id)
