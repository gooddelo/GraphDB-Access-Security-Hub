from src.entities.base import PermitDeniedException

class UserNotFoundException(PermitDeniedException):
    pass

class ObjectNotFoundException(PermitDeniedException):
    pass

class ObjectTypeError(TypeError):
    pass