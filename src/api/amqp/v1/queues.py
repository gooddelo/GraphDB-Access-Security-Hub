from faststream.rabbit import RabbitQueue


class UserQueuesV1:
    CREATE = RabbitQueue("v1.user_create", auto_delete=True)
    UPDATE = RabbitQueue("v1.user_update", auto_delete=True)
    DELETE = RabbitQueue("v1.user_delete", auto_delete=True)


class ScopeQueuesV1:
    CREATE = RabbitQueue("v1.scope_create", auto_delete=True)
    UPDATE = RabbitQueue("v1.scope_update", auto_delete=True)
    DELETE = RabbitQueue("v1.scope_delete", auto_delete=True)


class ResourceQueuesV1:
    CREATE = RabbitQueue("v1.resource_create", auto_delete=True)
    UPDATE = RabbitQueue("v1.resource_update", auto_delete=True)
    DELETE = RabbitQueue("v1.resource_delete", auto_delete=True)


class PermitQueuesV1:
    GET = RabbitQueue("v1.permit", auto_delete=True)
