from src.entities.policy.dal import PolicyDAO
from src.entities.user.dal import UserDAO
from src.entities.user.dto import UserPropertiesDTO
from src.entities.permit.dto import PermitRequestDTO
from src.entities.scope.dto import ScopePropertiesDTO
from src.entities.resource.dto import ResourcePropertiesDTO
from src.entities.base import PermitDeniedException
from src.entities.user.exceptions import UserNotFoundException
from src.entities.resource.exceptions import ResourceNotFoundException
from src.entities.scope.exceptions import ScopeAlreadyExistException
from src.entities.permit.exceptions import (
    SubjectNotFoundException,
    ObjectNotFoundException,
)


async def get_permit(data: PermitRequestDTO):
    object_attr = None
    if isinstance(data.object, UserPropertiesDTO):
        object_attr = data.object.role
    elif isinstance(data.object, ScopePropertiesDTO):
        object_attr = data.object.name
    elif isinstance(data.object, ResourcePropertiesDTO):
        object_attr = data.object.type
    try:
        permit_conditions = await PolicyDAO.get_permit_conditions(
            data.subject.role, object_attr, data.action
        )
        try:
            permit = await UserDAO.is_reachable(
                data.subject, data.object, **permit_conditions.model_dump(by_alias=True)
            )
        except UserNotFoundException as e:
            if e.user_id == data.subject.id_:
                raise SubjectNotFoundException(
                    subject=str(data.subject), object=str(data.object), action=data.action
                )
            else:
                raise ObjectNotFoundException(
                    subject=str(data.subject), object=str(data.object), action=data.action
                )
        except (ScopeAlreadyExistException, ResourceNotFoundException):
            raise ObjectNotFoundException(
                subject=str(data.subject), object=str(data.object), action=data.action
            )
    except PermitDeniedException:
        return False
    return permit
