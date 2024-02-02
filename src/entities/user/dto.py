import uuid
from typing import List
from src.entities.base import DTO


class UserCreateDTO(DTO):
    id: uuid.UUID
    role: str
    resource_ids: List[uuid.UUID]
    belong_namespace_ids: List[uuid.UUID]


class UserUpdateDTO(DTO):
    id: uuid.UUID
    new_role: str
    new_resource_ids: List[uuid.UUID]
    new_belong_namespace_ids: List[uuid.UUID]


class UserReadDTO(DTO):
    id: uuid.UUID
    role: str
