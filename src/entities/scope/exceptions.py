from src.entities.base import LOGGER

class ScopeNotFoundException(ValueError):
    def __init__(self, scope_id, name):
        self.scope_id = scope_id
        self.name = name
        super().__init__(f"Scope {self.scope_id} with name {self.name} doesn't exist")
        LOGGER.error(self)


class ScopeAlreadyExistException(ValueError):
    def __init__(self, scope_id, name):
        self.scope_id = scope_id
        self.name = name
        super().__init__(f"Scope {self.scope_id} with name {self.name} already exists")
        LOGGER.error(self)
