import structlog

LOGGER = structlog.get_logger()

class PermitDeniedException(Exception):
    def __init__(self, subject: str = "", object: str = "", action: str = ""):
        self.subject = subject
        self.object = object
        self.action = action
        super().__init__(
            f"Subj: {self.subject}; Obj: {self.object}; Act: {self.action};"
        )
        LOGGER.error(self)

