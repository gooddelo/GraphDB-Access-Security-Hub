import uuid

from pyneo4j_ogm import (  # type: ignore
    NodeModel,
    RelationshipProperty,
    RelationshipPropertyDirection,
    RelationshipPropertyCardinality,
)

from src.entities.resource.models import Resource
from src.entities.user.models import User
from src.relationships import Default


async def _check_uniqueness(self, *args, **kwargs):
    scope = await Scope.find_one({"scope_id": str(self.scope_id), "name": self.name})
    if scope is not None:
        raise ValueError(f"Scope {self.scope_id} with name {self.name} already exists")


class Scope(NodeModel):
    scope_id: uuid.UUID
    name: str

    owner: RelationshipProperty[User, Default] = RelationshipProperty(
        target_model=User,
        relationship_model=Default,
        direction=RelationshipPropertyDirection.INCOMING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_ONE,
        allow_multiple=False,
    )
    users: RelationshipProperty[User, Default] = RelationshipProperty(
        target_model=User,
        relationship_model=Default,
        direction=RelationshipPropertyDirection.OUTGOING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
    scopes: RelationshipProperty["Scope", Default] = RelationshipProperty(
        target_model="Scope",
        relationship_model=Default,
        direction=RelationshipPropertyDirection.OUTGOING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
    resources: RelationshipProperty[Resource, Default] = RelationshipProperty(
        target_model=Resource,
        relationship_model=Default,
        direction=RelationshipPropertyDirection.OUTGOING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )

    def __hash__(self):
        return hash(f"{self.scope_id}.{self.name}")

    class Settings:
        pre_hooks = {
            "create": _check_uniqueness,
            "update": _check_uniqueness,
        }
