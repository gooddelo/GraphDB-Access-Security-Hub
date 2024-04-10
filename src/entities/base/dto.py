from abc import ABC

from pydantic import BaseModel, ConfigDict


class DTO(BaseModel, ABC):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        arbitrary_types_allowed=False,
        extra="forbid",
    )


class PropertiesDTO(DTO, ABC):
    id_: str
    attr: str
