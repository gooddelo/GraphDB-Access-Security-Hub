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


class Namespace(NodeModel):
    namespace_id: uuid.UUID
    name: str

    users: RelationshipProperty[User, Default] = RelationshipProperty(
        target_model=User,
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
