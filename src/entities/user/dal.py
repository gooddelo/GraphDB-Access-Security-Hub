from pyneo4j_ogm import Pyneo4jClient # type: ignore

from src.entities.base import DAO
from src.entities.user.models import User, Resource, Namespace
from src.entities.user.dto import UserCreateDTO, UserReadDTO, UserUpdateDTO


class UserDAO(DAO):
    node_type: User

    @classmethod
    async def create(cls, client: Pyneo4jClient, data: UserCreateDTO):
        new = cls.node_type(
            **data.model_dump(exclude={"resource_ids", "new_belong_namespace_ids"})
        )
        await new.create()

        
