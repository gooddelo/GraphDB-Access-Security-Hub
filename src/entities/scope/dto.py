from typing import List, TypeVar, Generic

from pydantic import Field

from src.entities.base import DTO, PropertiesDTO
from src.entities.policy.models import Policy

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
    policy: Policy = Field(default_factory=dict)
    users: List[UserPropertiesDTO] = Field(default_factory=list)
    scopes: List[ScopePropertiesDTO] = Field(default_factory=list)
    resources: List[ResourcePropertiesDTO] = Field(default_factory=list)


class ScopeUpdateDTO(DTO, Generic[UserPropertiesDTO, ResourcePropertiesDTO]):
    id_: str
    old_name: str
    new_name: str | None = None
    new_users: List[UserPropertiesDTO] | None = None
    new_scopes: List[ScopePropertiesDTO] | None = None
    new_resources: List[ResourcePropertiesDTO] | None = None
