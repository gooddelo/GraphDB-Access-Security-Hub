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
    from src.entities.namespace.models import Namespace  # noqa
    from src.entities.user.models import User  # noqa


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
    namespaces: RelationshipProperty["Namespace", Default] = RelationshipProperty(
        target_model="Namespace",
        relationship_model=Default,
        direction=RelationshipPropertyDirection.INCOMING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
