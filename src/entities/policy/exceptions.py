from src.entities.base import PermitDeniedException


class SubjectRoleNotConfiguredError(PermitDeniedException):
    pass


class ActionNotAllowedError(PermitDeniedException):
    pass
