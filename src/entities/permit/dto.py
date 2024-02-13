from src.entities.base import DTO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO


class PermitRequestDTO(DTO):
    subject: UserPropertiesDTO
    object: ResourcePropertiesDTO | ScopePropertiesDTO | UserPropertiesDTO
    action: str
