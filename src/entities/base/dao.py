from abc import ABC, abstractmethod
from typing import Type

from pyneo4j_ogm import NodeModel  # type: ignore


class DAO(ABC):
    node_type: Type[NodeModel]

    @classmethod
    @abstractmethod
    async def create(cls, client, data):
        pass

    @classmethod
    @abstractmethod
    async def read(cls, client, id):
        pass

    @classmethod
    @abstractmethod
    async def update(cls):
        pass

    @classmethod
    @abstractmethod
    async def delete(cls):
        pass
