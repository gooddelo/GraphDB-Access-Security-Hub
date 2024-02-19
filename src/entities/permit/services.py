from src.entities.config.dal import ConfigDAO
from src.entities.user.dal import UserDAO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.permit.dto import PermitRequestDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO
from src.entities.base import PermitDeniedException

async def get_permit(data: PermitRequestDTO):
    object_attr = None
    if isinstance(data.object, UserPropertiesDTO):
        object_attr = data.object.role
    elif isinstance(data.object, ScopePropertiesDTO):
        object_attr = data.object.name
    elif isinstance(data.object, ResourcePropertiesDTO):
        object_attr = data.object.type
    try:
        permit_conditions = await ConfigDAO.get_permit_conditions(
            data.subject.role, object_attr, data.action
        )
        permit = await UserDAO.is_reachable(
            data.subject, data.object, **permit_conditions.model_dump()
        )
    except PermitDeniedException:
        return False
    return permit
