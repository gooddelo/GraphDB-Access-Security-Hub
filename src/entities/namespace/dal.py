import uuid

from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.namespace.dto import (
    NamespaceCreateDTO,
    NamespaceReadDTO,
    NamespaceUpdateDTO,
)
from src.entities.namespace.models import Namespace


class NamespaceDAO(DAO):
    node_type = Namespace

    @classmethod
    async def create(cls, data: NamespaceCreateDTO):
        new = cls.node_type(**data.model_dump(include={"namespace_id", "name"}))
        await new.create()
        owner = await User.find_one({"user_id": str(data.owner_id)})
        await new.owner.connect(owner)
        for user_id in data.user_ids:
            await new.users.connect(await User.find_one({"user_id": str(user_id)}))
        for namespace_id in data.namespace_ids:
            await new.namespaces.connect(
                await Namespace.find_one({"namespace_id": str(namespace_id)})
            )
        for resource_id in data.resource_ids:
            await new.resources.connect(
                await Resource.find_one({"resource_id": str(resource_id)})
            )

    @classmethod
    async def read(cls, id: uuid.UUID):
        namespace = await cls.node_type.find_one({"namespace_id": str(id)})
        return NamespaceReadDTO.from_orm(namespace)
