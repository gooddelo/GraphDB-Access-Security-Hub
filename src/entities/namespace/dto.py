import uuid
from typing import List

from pydantic import Field

from src.entities.base import DTO


class NamespaceCreateDTO(DTO):
    namespace_id: uuid.UUID = Field(...)
    name: str
    owner_id: uuid.UUID
    user_ids: List[uuid.UUID]
    namespace_ids: List[uuid.UUID]
    resource_ids: List[uuid.UUID]


class NamespaceUpdateDTO(DTO):
    namespace_id: uuid.UUID
    new_name: str
    new_owner_id: uuid.UUID
    new_user_ids: List[uuid.UUID]
    new_namespace_ids: List[uuid.UUID]
    new_resource_ids: List[uuid.UUID]


class NamespaceReadDTO(DTO):
    namespace_id: uuid.UUID
    name: str
