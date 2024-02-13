import uuid

from src.entities.scope.dal import ScopeDAO
from src.entities.scope.dto import ScopeCreateDTO, ScopeUpdateDTO


class ScopeService:
    dao = ScopeDAO

    @classmethod
    async def create(cls, scope_data: ScopeCreateDTO):
        return await cls.dao.create(scope_data)

    @classmethod
    async def update(cls, scope_data: ScopeUpdateDTO):
        return await cls.dao.update(scope_data)

    @classmethod
    async def delete(cls, scope_id: uuid.UUID):
        return await cls.dao.delete(scope_id)
