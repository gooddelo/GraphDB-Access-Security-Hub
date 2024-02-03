import uuid
from typing import List

from pydantic import Field
from src.entities.base import DTO


class UserCreateDTO(DTO):
    user_id: uuid.UUID = Field(...)
    role: str
    resource_ids: List[uuid.UUID]
    belong_namespace_ids: List[uuid.UUID]


class UserUpdateDTO(DTO):
    user_id: uuid.UUID
    new_role: str
    new_resource_ids: List[uuid.UUID]
    new_belong_namespace_ids: List[uuid.UUID]


class UserReadDTO(DTO):
    user_id: uuid.UUID
    role: str
