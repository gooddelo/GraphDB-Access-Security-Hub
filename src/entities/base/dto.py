from abc import ABC

from pydantic import BaseModel, ConfigDict


class DTO(BaseModel, ABC):
    model_config = ConfigDict(
        use_enum_values = True,
        arbitrary_types_allowed = False,
    )
