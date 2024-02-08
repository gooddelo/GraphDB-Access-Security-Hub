import uuid
from typing import List

from src.entities.base import DTO


class ScopeCreateDTO(DTO):
    scope_id: uuid.UUID
    name: str
    owner_id: uuid.UUID
    user_ids: List[uuid.UUID]
    scope_ids: List[uuid.UUID]
    resource_ids: List[uuid.UUID]


class ScopeUpdateDTO(DTO):
    scope_id: uuid.UUID
    new_name: str | None = None
    new_owner_id: uuid.UUID | None = None
    new_user_ids: List[uuid.UUID] | None = None
    new_scope_ids: List[uuid.UUID] | None = None
    new_resource_ids: List[uuid.UUID] | None = None


class ScopePropertiesDTO(DTO):
    scope_id: uuid.UUID
    name: str
