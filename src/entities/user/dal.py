import uuid
from typing import Set

from src.entities.base import DAO
from src.entities.resource.models import Resource
from src.entities.scope.models import Scope
from src.entities.user.models import User
from src.entities.user.dto import UserCreateDTO, UserPropertiesDTO, UserUpdateDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO
from src.entities.scope.exceptions import ScopeNotFoundException
from src.entities.resource.exceptions import ResourceNotFoundException
from src.entities.user.exceptions import (
    UserNotFoundException,
    UserAlreadyExistException,
    ObjectNotFoundException,
    ObjectTypeError,
)


class UserDAO(DAO):
    node_type = User

    @classmethod
    async def create(cls, data: UserCreateDTO):
        new = cls.node_type(id_=data.id_, attr=data.role)
        await new.create()
        for scope in data.belong_scopes:
            try:
                await new.belong_scopes.connect(
                    await Scope.find_one(scope.model_dump())
                )
                await new.own_scopes.connect(await Scope.find_one(scope.model_dump()))
            except AttributeError:
                print(type(scope))
                raise ScopeNotFoundException(scope.id_, scope.attr)
        for resource in data.resources:
            try:
                await new.resources.connect(
                    await Resource.find_one(resource.model_dump())
                )
            except AttributeError:
                raise ResourceNotFoundException(resource.id_, resource.attr)

    @classmethod
    async def update(cls, new_data: UserUpdateDTO):
        user = await cls.node_type.find_one({"id_": new_data.id_, "attr": new_data.old_role})
        if new_data.new_role is not None:
            user.role = new_data.new_role
            await user.update()
        if new_data.new_belong_scopes is not None:
            old_belong_scopes = {*(await user.belong_scopes.find_connected_nodes())}
            new_belong_scopes: Set[Scope] = {
                await Scope.find_one(scope.model_dump())
                for scope in new_data.new_belong_scopes
            }
            connect_belong_scopes = new_belong_scopes - old_belong_scopes
            disconnect_belong_scopes = old_belong_scopes - new_belong_scopes
            for scope in connect_belong_scopes:
                await user.belong_scopes.connect(scope)
                await user.own_scopes.connect(scope)
            for scope in disconnect_belong_scopes:
                await user.belong_scopes.disconnect(scope)
                await user.own_scopes.disconnect(scope)
        if new_data.new_resources is not None:
            old_resources = {*(await user.resources.find_connected_nodes())}
            new_resources: Set[Resource] = {
                await Resource.find_one(resource.model_dump())
                for resource in new_data.new_resources
            }
            connect_resources = new_resources - old_resources
            disconnect_resources = old_resources - new_resources
            for resource in connect_resources:
                await user.resources.connect(resource)
            for resource in disconnect_resources:
                await user.resources.disconnect(resource)

    @classmethod
    async def delete(cls, user_data: UserPropertiesDTO):
        user = await cls.node_type.find_one(user_data.model_dump())
        await user.delete()

    @classmethod
    async def is_reachable(
        cls,
        user_data: UserPropertiesDTO,
        object_data: UserPropertiesDTO | ScopePropertiesDTO | ResourcePropertiesDTO,
        max_depth: int | None = None,
    ):
        user = await cls.node_type.find_one(
            user_data.model_dump(mode="json", by_alias=True)
        )
        if user is None:
            raise UserNotFoundException(str(user_data))
        object_class = None
        if isinstance(object_data, UserPropertiesDTO):
            object_class = User
        elif isinstance(object_data, ScopePropertiesDTO):
            object_class = Scope
        elif isinstance(object_data, ResourcePropertiesDTO):
            object_class = Resource
        else:
            raise ObjectTypeError(type(object_data))
        object_ = await object_class.find_one(
            object_data.model_dump(mode="json", by_alias=True)
        )
        if object_ is None:
            raise ObjectNotFoundException(object=str(object_data))
        filters = {
            "$node": {
                "$labels": object_._settings.labels,
            }
        }
        if max_depth is not None:
            filters["$maxHops"] = max_depth  # type: ignore
        reachable_nodes = await user.find_connected_nodes(filters)
        return object_ in reachable_nodes
