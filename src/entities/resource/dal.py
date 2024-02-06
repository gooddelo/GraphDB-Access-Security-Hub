from src.entities.base import DAO
from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.namespace.models import Namespace
from src.entities.resource.dto import ResourceCreateDTO, ResourceUpdateDTO, ResourceReadDTO


class ResourceDAO(DAO):
    node_type = Resource

    @classmethod
    async def create(cls, data: ResourceCreateDTO):
        print(data)
        new = cls.node_type(**data.model_dump(include={"resource_id", "type"}))
        await new.create()
        for user_id in data.user_ids:
            await new.users.connect(await User.find_one({"user_id": str(user_id)}))
        for namespace_id in data.namespace_ids:
            await new.namespaces.connect(
                await Namespace.find_one({"namespace_id": str(namespace_id)})
            )