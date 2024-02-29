from src.entities.base import LOGGER

class UserAlreadyExistException(ValueError):
    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role
        super().__init__(f"User {self.user_id} with role {self.role} already exists")
        LOGGER.error(self)


class UserNotFoundException(ValueError):
    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role
        super().__init__(f"User {self.user_id} with role {self.role} doesn't exist")
        LOGGER.error(self)
