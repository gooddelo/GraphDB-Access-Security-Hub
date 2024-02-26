class ResourceNotFoundException(ValueError):
    def __init__(self, resource_id, type):
        self.resource_id = resource_id
        self.type = type
        super().__init__(f"Resource {self.resource_id} with type {self.type} doesn't exist")


class ResourceAlreadyExistException(ValueError):
    def __init__(self, resource_id, type):
        self.resource_id = resource_id
        self.type = type
        super().__init__(f"Resource {self.resource_id} with type {self.type} already exists")
