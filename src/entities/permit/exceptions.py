from src.entities.base import PermitDeniedException, LOGGER


class SubjectNotFoundException(PermitDeniedException):
    pass


class ObjectNotFoundException(PermitDeniedException):
    pass


class ObjectTypeError(TypeError):
    def __init__(self, *args):
        super().__init__(*args)
        LOGGER.error(self)

class SubjectRoleNotConfiguredError(PermitDeniedException):
    pass


class ActionNotAllowedError(PermitDeniedException):
    pass
