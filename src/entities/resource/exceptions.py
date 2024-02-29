from src.entities.base import LOGGER

class ResourceNotFoundException(ValueError):
    def __init__(self, resource_id, type):
        self.resource_id = resource_id
        self.type = type
        super().__init__(
            f"Resource {self.resource_id} with type {self.type} doesn't exist"
        )
        LOGGER.error(self)


class ResourceAlreadyExistException(ValueError):
    def __init__(self, resource_id, type):
        self.resource_id = resource_id
        self.type = type
        super().__init__(
            f"Resource {self.resource_id} with type {self.type} already exists"
        )
        LOGGER.error(self)
