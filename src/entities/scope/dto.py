from typing import List

from pydantic import Field

from src.entities.base import DTO, PropertiesDTO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


class ScopePropertiesDTO(PropertiesDTO):
    attr: str = Field(validation_alias="name")

    @property
    def name(self) -> str:
        return self.attr


class ScopeCreateDTO(DTO):
    id_: str
    name: str
    owner: UserPropertiesDTO
    users: List[UserPropertiesDTO] = Field(default_factory=list)
    scopes: List[ScopePropertiesDTO] = Field(default_factory=list)
    resources: List[ResourcePropertiesDTO] = Field(default_factory=list)


class ScopeUpdateDTO(DTO):
    id_: str
    old_name: str
    new_name: str | None = None
    new_owner: UserPropertiesDTO | None = None
    new_users: List[UserPropertiesDTO] | None = None
    new_scopes: List[ScopePropertiesDTO] | None = None
    new_resources: List[ResourcePropertiesDTO] | None = None
