import uuid

from src.entities.resource.dal import ResourceDAO
from src.entities.resource.dto import ResourceCreateDTO, ResourceUpdateDTO


class ResourceService:
    dao = ResourceDAO

    @classmethod
    async def create(cls, resource_data: ResourceCreateDTO):
        return await cls.dao.create(resource_data)

    @classmethod
    async def update(cls, resource_data: ResourceUpdateDTO):
        return await cls.dao.update(resource_data)

    @classmethod
    async def delete(cls, resource_id: uuid.UUID):
        return await cls.dao.delete(resource_id)