from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.namespace.models import Namespace
from src.entities.resource.models import Resource
from src.entities.user.dto import UserCreateDTO, UserReadDTO, UserUpdateDTO


class UserDAO(DAO):
    node_type = User

    @classmethod
    async def create(cls, data: UserCreateDTO):
        new: User = cls.node_type(**data.model_dump(include={"user_id", "role"}))
        await new.create()
        for namespace_id in data.belong_namespace_ids:
            await new.belong_namespaces.connect(
                await Namespace.find_one({"namespace_id": str(namespace_id)})
            )
            await new.own_namespaces.connect(
                await Namespace.find_one({"namespace_id": str(namespace_id)})
            )
        for resource_id in data.resource_ids:
            await new.resources.connect(
                await Resource.find_one({"resource_id": str(resource_id)})
            )
