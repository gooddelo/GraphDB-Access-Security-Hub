from abc import ABC
from typing import Type, ClassVar

from pydantic import Field
from pyneo4j_ogm import NodeModel  # type: ignore[import]


async def _check_uniqueness(self, *args, **kwargs):
    cls = type(self)
    resource = await cls.find_one({"id_": str(self.id_), "attr": self.attr})
    if resource is not None:
        raise self.exists_exception(self.id_, self.attr)


class BaseNode(NodeModel, ABC):
    id_: str = Field(...)
    attr: str = Field(...)
    exists_exception: ClassVar[Type[Exception]]
    not_found_exception: ClassVar[Type[Exception]]

    def __hash__(self):
        return hash(f"{self.id_}.{self.attr}")

    class Settings:
        pre_hooks = {
            "create": _check_uniqueness,
            "update": _check_uniqueness,
        }
