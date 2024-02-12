import uuid

from src.entities.base import DAO
from src.entities.user import User
from src.entities.resource import Resource
from src.entities.scope import (
    Scope,
    ScopeCreateDTO,
    ScopePropertiesDTO,
    ScopeUpdateDTO,
)


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
        return ScopePropertiesDTO.from_orm(scope)

    @classmethod
    async def update(cls, new_data: ScopeUpdateDTO):
        scope = await cls.node_type.find_one({"scope_id": str(new_data.scope_id)})
        if new_data.new_name is not None:
            scope.name = new_data.new_name
            await scope.update()
        if new_data.new_owner_id is not None:
            await scope.owner.disconnect_all()
            owner = await User.find_one({"user_id": str(new_data.new_owner_id)})
            await scope.owner.connect(owner)
        if new_data.new_user_ids is not None:
            old_users = {*(await scope.users.find_connected_nodes())}
            new_users = {
                await User.find_one({"user_id": str(user_id)})
                for user_id in new_data.new_user_ids
            }
            connect_users = new_users - old_users
            disconnect_users = old_users - new_users
            for user in connect_users:
                await scope.users.connect(user)
                await user.own_scopes.connect(scope)
            for user in disconnect_users:
                await scope.users.disconnect(user)
                await user.own_scopes.disconnect(scope)
        if new_data.new_resource_ids is not None:
            old_resources = {*(await scope.resources.find_connected_nodes())}
            new_resources = {
                await Resource.find_one({"resource_id": str(resource_id)})
                for resource_id in new_data.new_resource_ids
            }
            connect_resources = new_resources - old_resources
            disconnect_resources = old_resources - new_resources
            for resource in connect_resources:
                await scope.resources.connect(resource)
            for resource in disconnect_resources:
                await scope.resources.disconnect(resource)
        if new_data.new_scope_ids is not None:
            old_scopes = {*(await scope.scopes.find_connected_nodes())}
            new_scopes = {
                await Scope.find_one({"scope_id": str(scope_id)})
                for scope_id in new_data.new_scope_ids
            }
            connect_scopes = new_scopes - old_scopes
            disconnect_scopes = old_scopes - new_scopes
            for scope_ in connect_scopes:
                await scope.scopes.connect(scope_)
            for scope_ in disconnect_scopes:
                await scope.scopes.disconnect(scope_)

    @classmethod
    async def delete(self, id: uuid.UUID):
        scope = await self.node_type.find_one({"scope_id": str(id)})
        await scope.delete()
