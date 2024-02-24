from abc import ABC

from pydantic import Field
from pyneo4j_ogm import NodeModel  # type: ignore[import]


async def _check_uniqueness(self, *args, **kwargs):
    cls = type(self)
    resource = await cls.find_one({"id_": str(self.id_), "attr": self.attr})
    if resource is not None:
        raise ValueError(
            f"{cls.__name__} {self.id_} with attr {self.attr} already exists"
        )


class BaseNode(NodeModel, ABC):
    id_: str = Field(...)
    attr: str = Field(...)

    def __hash__(self):
        return hash(f"{self.id_}.{self.attr}")

    class Settings:
        pre_hooks = {
            "create": _check_uniqueness,
            "update": _check_uniqueness,
        }
