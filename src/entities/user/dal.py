import uuid
from typing import Set

from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.scope.models import Scope
from src.entities.resource.models import Resource
from src.entities.user.dto import UserCreateDTO, UserReadDTO, UserUpdateDTO


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
        return UserReadDTO.from_orm(user)

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
