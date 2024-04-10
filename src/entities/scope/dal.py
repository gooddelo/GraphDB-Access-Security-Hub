from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.scope.dto import (
    ScopeCreateDTO,
    ScopePropertiesDTO,
    ScopeUpdateDTO,
)
from src.entities.scope.models import Scope


class ScopeDAO(DAO):
    node_type = Scope

    @classmethod
    async def create(cls, data: ScopeCreateDTO):
        new = cls.node_type(id_=data.id_, attr=data.name, policy=data.policy)
        await new.create()
        for user in data.users:
            await new.users.connect(await User.find_one(user.model_dump()))
        for scope in data.scopes:
            await new.scopes.connect(await Scope.find_one(scope.model_dump()))
        for resource in data.resources:
            await new.resources.connect(await Resource.find_one(resource.model_dump()))

    @classmethod
    async def update(cls, new_data: ScopeUpdateDTO):
        scope = await cls.node_type.find_one(
            {"id_": new_data.id_, "attr": new_data.old_name}
        )
        if scope is None:
            raise cls.node_type.not_found_exception(
                scope_id=new_data.id_, name=new_data.old_name
            )
        if new_data.new_name is not None:
            scope.name = new_data.new_name
            await scope.update()
        if new_data.new_users is not None:
            old_users = {*(await scope.users.find_connected_nodes())}
            new_users = {
                await User.find_one(user.model_dump()) for user in new_data.new_users
            }
            connect_users = new_users - old_users
            disconnect_users = old_users - new_users
            for user in connect_users:
                await scope.users.connect(user)
                await user.own_scopes.connect(scope)
            for user in disconnect_users:
                await scope.users.disconnect(user)
                await user.own_scopes.disconnect(scope)
        if new_data.new_resources is not None:
            old_resources = {*(await scope.resources.find_connected_nodes())}
            new_resources = {
                await Resource.find_one(resource.model_dump())
                for resource in new_data.new_resources
            }
            connect_resources = new_resources - old_resources
            disconnect_resources = old_resources - new_resources
            for resource in connect_resources:
                await scope.resources.connect(resource)
            for resource in disconnect_resources:
                await scope.resources.disconnect(resource)
        if new_data.new_scopes is not None:
            old_scopes = {*(await scope.scopes.find_connected_nodes())}
            new_scopes = {
                await Scope.find_one(scope.model_dump())
                for scope in new_data.new_scopes
            }
            connect_scopes = new_scopes - old_scopes
            disconnect_scopes = old_scopes - new_scopes
            for scope_ in connect_scopes:
                await scope.scopes.connect(scope_)
            for scope_ in disconnect_scopes:
                await scope.scopes.disconnect(scope_)

    @classmethod
    async def delete(cls, scope_data: ScopePropertiesDTO):
        scope = await cls.node_type.find_one(scope_data.model_dump())
        try:
            await scope.delete()
        except AttributeError:
            raise cls.node_type.not_found_exception(scope_data.id_, scope_data.name)
