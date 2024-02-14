from pydantic import Field

from src.entities.base import DTO

class ConditionsDTO(DTO):
    max_depth: int = Field(ge=1)