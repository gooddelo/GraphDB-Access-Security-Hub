import uuid
from typing import List

from src.entities.base import DTO


class ResourceCreateDTO(DTO):
    resource_id: uuid.UUID
    type: str
    user_ids: List[uuid.UUID]
    scope_ids: List[uuid.UUID]


class ResourceUpdateDTO(DTO):
    resource_id: uuid.UUID
    new_type: str | None = None
    new_user_ids: List[uuid.UUID] | None = None
    new_scope_ids: List[uuid.UUID] | None = None


class ResourceReadDTO(DTO):
    resource_id: uuid.UUID
    type: str
