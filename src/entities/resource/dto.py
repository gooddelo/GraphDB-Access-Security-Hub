from typing import List, TypeVar, Generic

from pydantic import Field

from src.entities.base import DTO, PropertiesDTO


UserPropertiesDTO = TypeVar("UserPropertiesDTO", bound=PropertiesDTO)
ScopePropertiesDTO = TypeVar("ScopePropertiesDTO", bound=PropertiesDTO)


class ResourceCreateDTO(DTO, Generic[UserPropertiesDTO, ScopePropertiesDTO]):
    id_: str
    type: str
    users: List[UserPropertiesDTO]
    scopes: List[ScopePropertiesDTO]


class ResourceUpdateDTO(DTO, Generic[UserPropertiesDTO, ScopePropertiesDTO]):
    id_: str
    old_type: str
    new_type: str | None = None
    new_users: List[UserPropertiesDTO] | None = None
    new_scopes: List[ScopePropertiesDTO] | None = None


class ResourcePropertiesDTO(PropertiesDTO):
    attr: str = Field(validation_alias="type")

    @property
    def type(self) -> str:
        return self.attr
