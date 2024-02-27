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
        new = cls.node_type(id_=data.id_, attr=data.type)
        await new.create()
        for user in data.users:
            await new.users.connect(await User.find_one(user.model_dump()))
        for scope in data.scopes:
            await new.scopes.connect(await Scope.find_one(scope.model_dump()))

    @classmethod
    async def read(cls, id: uuid.UUID):
        resource = await cls.node_type.find_one({"resource_id": str(id)})
        return ResourcePropertiesDTO.model_validate(resource)

    @classmethod
    async def update(cls, new_data: ResourceUpdateDTO):
        resource = await cls.node_type.find_one(
            {"id_": new_data.id_, "attr": new_data.old_type}
        )
        if new_data.new_type is not None:
            resource.type = new_data.new_type
            await resource.update()
        if new_data.new_users is not None:
            old_users = set(await resource.users.find_connected_nodes())
            new_users = {
                await User.find_one(user.model_dump())
                for user in new_data.new_users
            }
            connect_users = new_users - old_users
            disconnect_users = old_users - new_users
            for user in connect_users:
                await resource.users.connect(user)
            for user in disconnect_users:
                await resource.users.disconnect(user)
        if new_data.new_scopes is not None:
            old_scopes = set(await resource.scopes.find_connected_nodes())
            new_scopes = {
                await Scope.find_one(scope.model_dump())
                for scope in new_data.new_scopes
            }
            connect_scopes = new_scopes - old_scopes
            disconnect_scopes = old_scopes - new_scopes
            for scope in connect_scopes:
                await resource.scopes.connect(scope)
            for scope in disconnect_scopes:
                await resource.scopes.disconnect(scope)

    @classmethod
    async def delete(cls, resource_data: ResourcePropertiesDTO):
        resource = await cls.node_type.find_one(resource_data.model_dump())
        try:
            await resource.delete()
        except AttributeError:
            raise cls.node_type.not_found_exception(resource_data.id_, resource_data.type)
