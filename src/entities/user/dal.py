import uuid
from typing import Set

from src.entities.base import DAO
from src.entities.scope import Scope, ScopePropertiesDTO
from src.entities.resource import Resource, ResourcePropertiesDTO
from src.entities.user import User, UserCreateDTO, UserPropertiesDTO, UserUpdateDTO


class UserDAO(DAO):
    node_type = User

    @classmethod
    async def create(cls, data: UserCreateDTO):
        new: User = cls.node_type(**data.model_dump(include={"user_id", "role"}))
        await new.create()
        for scope_id in data.belong_scope_ids:
            await new.belong_scopes.connect(
                await Scope.find_one({"scope_id": str(scope_id)})
            )
            await new.own_scopes.connect(
                await Scope.find_one({"scope_id": str(scope_id)})
            )
        for resource_id in data.resource_ids:
            await new.resources.connect(
                await Resource.find_one({"resource_id": str(resource_id)})
            )

    @classmethod
    async def read(cls, id: uuid.UUID):
        user = await cls.node_type.find_one({"user_id": str(id)})
        return UserPropertiesDTO.from_orm(user)

    @classmethod
    async def update(cls, new_data: UserUpdateDTO):
        user = await cls.node_type.find_one({"user_id": str(new_data.user_id)})
        if new_data.new_role is not None:
            user.role = new_data.new_role
            await user.update()
        if new_data.new_belong_scope_ids is not None:
            old_belong_scopes = {*(await user.belong_scopes.find_connected_nodes())}
            new_belong_scopes: Set[Scope] = {
                await Scope.find_one({"scope_id": str(scope_id)})
                for scope_id in new_data.new_belong_scope_ids
            }
            connect_belong_scopes = new_belong_scopes - old_belong_scopes
            disconnect_belong_scopes = old_belong_scopes - new_belong_scopes
            for scope in connect_belong_scopes:
                await user.belong_scopes.connect(scope)
                await user.own_scopes.connect(scope)
            for scope in disconnect_belong_scopes:
                await user.belong_scopes.disconnect(scope)
                await user.own_scopes.disconnect(scope)
        if new_data.new_resource_ids is not None:
            old_resources = {*(await user.resources.find_connected_nodes())}
            new_resources: Set[Resource] = {
                await Resource.find_one({"resource_id": str(resource_id)})
                for resource_id in new_data.new_resource_ids
            }
            connect_resources = new_resources - old_resources
            disconnect_resources = old_resources - new_resources
            for resource in connect_resources:
                await user.resources.connect(resource)
            for resource in disconnect_resources:
                await user.resources.disconnect(resource)

    @classmethod
    async def delete(cls, id: uuid.UUID):
        user = await cls.node_type.find_one({"user_id": str(id)})
        await user.delete()

    @classmethod
    async def is_reachable(
        cls,
        user_data: UserPropertiesDTO,
        object_data: UserPropertiesDTO | ScopePropertiesDTO | ResourcePropertiesDTO,
    ):
        user = await cls.node_type.find_one(user_data.model_dump(mode='json'))
        object_class = None
        if isinstance(object_data, UserPropertiesDTO):
            object_class = User
        elif isinstance(object_data, ScopePropertiesDTO):
            object_class = Scope
        elif isinstance(object_data, ResourcePropertiesDTO):
            object_class = Resource
        object_ = await object_class.find_one(
            object_data.model_dump(mode='json')
        )
        reachable_nodes = await user.find_connected_nodes(
            {
                "$node": {
                    "$labels": object_._settings.labels,
                }
            }
        )
        return object_ in reachable_nodes
