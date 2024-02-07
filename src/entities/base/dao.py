from abc import ABC, abstractmethod
from typing import Type

from pyneo4j_ogm import NodeModel  # type: ignore


class DAO(ABC):
    node_type: Type[NodeModel]

    @classmethod
    @abstractmethod
    async def create(cls, data):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def read(cls, id):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def update(cls):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete(cls):
        raise NotImplementedError()
