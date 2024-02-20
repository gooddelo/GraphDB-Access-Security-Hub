from pydantic import Field

from src.entities.base import DTO


class ConditionsDTO(DTO):
    max_depth: int | None = Field(default=None, ge=1)
