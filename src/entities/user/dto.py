from typing import List, TypeVar, Generic

from pydantic import Field

from src.entities.base import DTO, PropertiesDTO


ScopePropertiesDTO = TypeVar("ScopePropertiesDTO", bound=PropertiesDTO)
ResourcePropertiesDTO = TypeVar("ResourcePropertiesDTO", bound=PropertiesDTO)


class UserCreateDTO(DTO, Generic[ScopePropertiesDTO, ResourcePropertiesDTO]):
    id_: str
    role: str
    resources: List[ResourcePropertiesDTO] = Field(default_factory=list)
    belong_scopes: List[ScopePropertiesDTO] = Field(default_factory=list)


class UserUpdateDTO(DTO, Generic[ScopePropertiesDTO, ResourcePropertiesDTO]):
    id_: str
    old_role: str
    new_role: str | None = None
    new_resources: List[ResourcePropertiesDTO] | None = None
    new_belong_scopes: List[ScopePropertiesDTO] | None = None


class UserPropertiesDTO(PropertiesDTO):
    attr: str = Field(validation_alias="role")

    @property
    def role(self):
        return self.attr
