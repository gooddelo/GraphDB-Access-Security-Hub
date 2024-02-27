class RoleNotConfiguredError(Exception):
    def __init__(self, role):
        self.role = role
        super().__init__(f"Role '{self.role}' is not configured in policy")


class ActionNotConfiguredError(Exception):
    def __init__(self, role, type_, action):
        self.role = role
        self.type = type_
        self.action = action
        super().__init__(
            f"Action '{self.action}' is not configured for role '{self.role}' on object type '{self.type}'"
        )
