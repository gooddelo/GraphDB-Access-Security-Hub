import uuid

from pyneo4j_ogm import (  # type: ignore
    NodeModel,
    RelationshipProperty,
    RelationshipPropertyDirection,
    RelationshipPropertyCardinality,
)

from src.entities.resource.models import Resource
from src.entities.user.models import User
from src.relationships.default import Default


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