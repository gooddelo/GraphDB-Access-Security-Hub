from pydantic import Field

from src.entities.base import DTO

class ConditionsDTO(DTO):
    depth: int = Field(ge=1)