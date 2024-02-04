from pyneo4j_ogm import Pyneo4jClient  # type: ignore

from src.entities.base import DAO
from src.entities.namespace.models import Namespace
from src.entities.namespace.dto import (
    NamespaceCreateDTO,
    NamespaceReadDTO,
    NamespaceUpdateDTO,
)


class NamespaceDAO(DAO):
    node_type = Namespace

    @classmethod
    async def create(cls, client: Pyneo4jClient, data: NamespaceCreateDTO):
        new = cls.node_type(**data.model_dump(include={"namespace_id", "name"}))
        await new.create()
