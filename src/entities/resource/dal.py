import uuid

from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.scope.models import Scope
from src.entities.resource.dto import (
    ResourceCreateDTO,
    ResourceUpdateDTO,
    ResourcePropertiesDTO,
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
        return ResourcePropertiesDTO.model_validate(resource)

    @classmethod
    async def update(cls, new_data: ResourceUpdateDTO):
        resource = await cls.node_type.find_one(
            {"resource_id": str(new_data.resource_id)}
        )
        if new_data.new_type is not None:
            resource.type = new_data.new_type
            await resource.update()
        if new_data.new_user_ids is not None:
            old_users = set(await resource.users.find_connected_nodes())
            new_users = {
                await User.find_one({"user_id": str(user_id)})
                for user_id in new_data.new_user_ids
            }
            connect_users = new_users - old_users
            disconnect_users = old_users - new_users
            for user in connect_users:
                await resource.users.connect(user)
            for user in disconnect_users:
                await resource.users.disconnect(user)
        if new_data.new_scope_ids is not None:
            old_scopes = set(await resource.scopes.find_connected_nodes())
            new_scopes = {
                await Scope.find_one({"scope_id": str(scope_id)})
                for scope_id in new_data.new_scope_ids
            }
            connect_scopes = new_scopes - old_scopes
            disconnect_scopes = old_scopes - new_scopes
            for scope in connect_scopes:
                await resource.scopes.connect(scope)
            for scope in disconnect_scopes:
                await resource.scopes.disconnect(scope)

    @classmethod
    async def delete(cls, id: uuid.UUID):
        resource = await cls.node_type.find_one({"resource_id": str(id)})
        await resource.delete()
