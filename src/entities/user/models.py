import uuid
import typing

from pyneo4j_ogm import (
    NodeModel,
    RelationshipProperty,
    RelationshipPropertyDirection,
    RelationshipPropertyCardinality,
)  # type: ignore

from src.entities.resource.models import Resource
from src.relationships.default import Default


if typing.TYPE_CHECKING:
    from src.entities.namespace.models import Namespace  # noqa


def _namespace():
    from src.entities.namespace.models import Namespace

    return Namespace


class User(NodeModel):
    id = uuid.UUID
    role = str

    resources: RelationshipProperty[Resource, Default] = RelationshipProperty(
        target_model=_namespace(),
        relationship_model=Default,
        direction=RelationshipPropertyDirection.OUTGOING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
    own_namespaces: RelationshipProperty[_namespace(), Default] = RelationshipProperty(
        target_model="Namespace",
        relationship_model=Default,
        direction=RelationshipPropertyDirection.OUTGOING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
    belong_namespaces: RelationshipProperty[
        _namespace(), Default
    ] = RelationshipProperty(
        target_model=_namespace(),
        relationship_model=Default,
        direction=RelationshipPropertyDirection.INCOMING,
        cardinality=RelationshipPropertyCardinality.ZERO_OR_MORE,
        allow_multiple=False,
    )
