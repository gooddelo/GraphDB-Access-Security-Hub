import uuid
from typing import List

from pydantic import Field

from src.entities.base import DTO


class UserCreateDTO(DTO):
    user_id: uuid.UUID = Field(...)
    role: str
    resource_ids: List[uuid.UUID]
    belong_scope_ids: List[uuid.UUID]


class UserUpdateDTO(DTO):
    user_id: uuid.UUID
    new_role: str | None = None
    new_resource_ids: List[uuid.UUID] | None = None
    new_belong_scope_ids: List[uuid.UUID] | None = None


class UserPropertiesDTO(DTO):
    user_id: uuid.UUID
    role: str
