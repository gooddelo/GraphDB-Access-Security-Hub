import uuid
import typing

from pyneo4j_ogm import (  # type: ignore
    NodeModel,
    RelationshipProperty,
    RelationshipPropertyDirection,
    RelationshipPropertyCardinality,
)

from src.entities.resource.models import Resource
from src.relationships.default import Default


if typing.TYPE_CHECKING:
    from src.entities.namespace.models import Namespace  # noqa


class User(NodeModel):
    user_id: uuid.UUID
    role: str

    resources: RelationshipProperty[Resource, Default] = RelationshipProperty(
        target_model=Resource,
        relationship_model=Default,
        direction=RelationshipPropertyDirection.OUTGOING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
    own_namespaces: RelationshipProperty["Namespace", Default] = RelationshipProperty(
        target_model="Namespace",
        relationship_model=Default,
        direction=RelationshipPropertyDirection.OUTGOING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
    belong_namespaces: RelationshipProperty[
        "Namespace", Default
    ] = RelationshipProperty(
        target_model="Namespace",
        relationship_model=Default,
        direction=RelationshipPropertyDirection.INCOMING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
