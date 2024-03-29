from abc import ABC, abstractmethod
from typing import Type, ClassVar

from pyneo4j_ogm import NodeModel  # type: ignore


class DAO(ABC):
    node_type: ClassVar[Type[NodeModel]]

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
    async def update(cls, new_data):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    async def delete(cls, id):
        raise NotImplementedError()
