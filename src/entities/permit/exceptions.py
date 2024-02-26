from src.entities.base import PermitDeniedException


class SubjectNotFoundException(PermitDeniedException):
    pass


class ObjectNotFoundException(PermitDeniedException):
    pass


class ObjectTypeError(TypeError):
    pass
