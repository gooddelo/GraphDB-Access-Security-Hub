import uuid

from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.scope.models import Scope
from src.entities.resource.dto import (
    ResourceCreateDTO,
    ResourceUpdateDTO,
    ResourceReadDTO,
)


class ResourceDAO(DAO):
    node_type = Resource

    @classmethod
    async def create(cls, data: ResourceCreateDTO):
        print(data)
        new = cls.node_type(**data.model_dump(include={"resource_id", "type"}))
        await new.create()
        for user_id in data.user_ids:
            await new.users.connect(await User.find_one({"user_id": str(user_id)}))
        for scope_id in data.scope_ids:
            await new.scopes.connect(await Scope.find_one({"scope_id": str(scope_id)}))

    @classmethod
    async def read(cls, id: uuid.UUID):
        resource = await cls.node_type.find_one({"resource_id": str(id)})
        return ResourceReadDTO.from_orm(resource)
