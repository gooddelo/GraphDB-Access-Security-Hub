import uuid
from typing import List

from pydantic import Field

from src.entities.base import DTO


class ScopeCreateDTO(DTO):
    scope_id: uuid.UUID = Field(...)
    name: str
    owner_id: uuid.UUID
    user_ids: List[uuid.UUID]
    scope_ids: List[uuid.UUID]
    resource_ids: List[uuid.UUID]


class ScopeUpdateDTO(DTO):
    scope_id: uuid.UUID
    new_name: str
    new_owner_id: uuid.UUID
    new_user_ids: List[uuid.UUID]
    new_scope_ids: List[uuid.UUID]
    new_resource_ids: List[uuid.UUID]


class ScopeReadDTO(DTO):
    scope_id: uuid.UUID
    name: str
