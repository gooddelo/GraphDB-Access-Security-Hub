import uuid
from typing import List

from pydantic import Field

from src.entities.base import DTO


class ResourceCreateDTO(DTO):
    resource_id: uuid.UUID = Field(...)
    type: str
    user_ids: List[uuid.UUID]
    namespace_ids: List[uuid.UUID]


class ResourceUpdateDTO(DTO):
    resource_id: uuid.UUID
    new_type: str
    new_user_ids: List[uuid.UUID]
    new_namespace_ids: List[uuid.UUID]


class ResourceReadDTO(DTO):
    resource_id: uuid.UUID
    type: str
