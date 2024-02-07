import uuid

from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.scope.dto import (
    ScopeCreateDTO,
    ScopeReadDTO,
    ScopeUpdateDTO,
)
from src.entities.scope.models import Scope


class ScopeDAO(DAO):
    node_type = Scope

    @classmethod
    async def create(cls, data: ScopeCreateDTO):
        new = cls.node_type(**data.model_dump(include={"scope_id", "name"}))
        await new.create()
        owner = await User.find_one({"user_id": str(data.owner_id)})
        await new.owner.connect(owner)
        for user_id in data.user_ids:
            await new.users.connect(await User.find_one({"user_id": str(user_id)}))
        for scope_id in data.scope_ids:
            await new.scopes.connect(await Scope.find_one({"scope_id": str(scope_id)}))
        for resource_id in data.resource_ids:
            await new.resources.connect(
                await Resource.find_one({"resource_id": str(resource_id)})
            )

    @classmethod
    async def read(cls, id: uuid.UUID):
        scope = await cls.node_type.find_one({"scope_id": str(id)})
        return ScopeReadDTO.from_orm(scope)
