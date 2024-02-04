from pyneo4j_ogm import Pyneo4jClient  # type: ignore

from src.entities.base import DAO
from src.entities.resource.models import Resource
from src.entities.resource.dto import ResourceCreateDTO, ResourceUpdateDTO, ResourceReadDTO


class ResourceDAO(DAO):
    node_type = Resource

    @classmethod
    async def create(cls, client: Pyneo4jClient, data: ResourceCreateDTO):
        new = cls.node_type(**data.model_dump(include={"resource_id", "type"}))
        await new.create()
