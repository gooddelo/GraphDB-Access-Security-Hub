import uuid
import typing

from pyneo4j_ogm import (  # type: ignore
    NodeModel,
    RelationshipProperty,
    RelationshipPropertyDirection,
    RelationshipPropertyCardinality,
)

from src.relationships.default import Default


if typing.TYPE_CHECKING:
    from src.entities.scope.models import Scope  # noqa
    from src.entities.user.models import User  # noqa


async def _check_uniqueness(self, *args, **kwargs):
    resource = await Resource.find_one({"resource_id": str(self.resource_id), "type": self.type})
    if resource is not None:
        raise ValueError(f"Resource {self.resource_id} with type {self.type} already exists")


class Resource(NodeModel):
    resource_id: uuid.UUID
    type: str
    users: RelationshipProperty["User", Default] = RelationshipProperty(
        target_model="User",
        relationship_model=Default,
        direction=RelationshipPropertyDirection.INCOMING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
    scopes: RelationshipProperty["Scope", Default] = RelationshipProperty(
        target_model="Scope",
        relationship_model=Default,
        direction=RelationshipPropertyDirection.INCOMING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )

    def __hash__(self):
        return hash(f"{self.resource_id}.{self.type}")

    class Settings:
        pre_hooks = {
            "create": _check_uniqueness,
            "update": _check_uniqueness,
        }