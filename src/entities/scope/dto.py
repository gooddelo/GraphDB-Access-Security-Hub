from typing import List, TypeVar, Generic

from pydantic import Field

from src.entities.base import DTO, PropertiesDTO


UserPropertiesDTO = TypeVar("UserPropertiesDTO", bound=PropertiesDTO)
ResourcePropertiesDTO = TypeVar("ResourcePropertiesDTO", bound=PropertiesDTO)


class ScopePropertiesDTO(PropertiesDTO):
    attr: str = Field(validation_alias="name")

    @property
    def name(self) -> str:
        return self.attr


class ScopeCreateDTO(DTO, Generic[UserPropertiesDTO, ResourcePropertiesDTO]):
    id_: str
    name: str
    owner: UserPropertiesDTO
    users: List[UserPropertiesDTO]
    scopes: List[ScopePropertiesDTO]
    resources: List[ResourcePropertiesDTO]


class ScopeUpdateDTO(DTO, Generic[UserPropertiesDTO, ResourcePropertiesDTO]):
    id_: str
    old_name: str
    new_name: str | None = None
    new_owner: UserPropertiesDTO | None = None
    new_users: List[UserPropertiesDTO] | None = None
    new_scopes: List[ScopePropertiesDTO] | None = None
    new_resources: List[ResourcePropertiesDTO] | None = None
