from pyneo4j_ogm import Pyneo4jClient # type: ignore

from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.namespace.models import Namespace
from src.entities.resource.models import Resource
from src.entities.user.dto import UserCreateDTO, UserReadDTO, UserUpdateDTO


class UserDAO(DAO):
    node_type = User

    @classmethod
    async def create(cls, client: Pyneo4jClient, data: UserCreateDTO):
        new = cls.node_type(
            **data.model_dump(include={"user_id", "role"})
        )
        await new.create()

        
