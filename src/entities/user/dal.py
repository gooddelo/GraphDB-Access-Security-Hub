import uuid
from typing import Set

from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.scope.models import Scope
from src.entities.resource.models import Resource
from src.entities.user.dto import UserCreateDTO, UserPropertiesDTO, UserUpdateDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


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
        max_depth: int | None = None,
    ):
        user = await cls.node_type.find_one(user_data.model_dump(mode="json"))
        if user is None:
            raise ValueError(f"{cls.node_type.__name__} not found")
        object_class = None
        if isinstance(object_data, UserPropertiesDTO):
            object_class = User
        elif isinstance(object_data, ScopePropertiesDTO):
            object_class = Scope
        elif isinstance(object_data, ResourcePropertiesDTO):
            object_class = Resource
        else:
            raise ValueError(f"Unknown object type: {type(object_data)}")
        object_ = await object_class.find_one(object_data.model_dump(mode="json"))
        if object_ is None:
            raise ValueError(f"{object_class.__name__} not found")
        filters = {
            "$node": {
                "$labels": object_._settings.labels,
            }
        }
        if max_depth is not None:
            filters["$maxHops"] = max_depth  # type: ignore
        reachable_nodes = await user.find_connected_nodes(filters)
        return object_ in reachable_nodes
