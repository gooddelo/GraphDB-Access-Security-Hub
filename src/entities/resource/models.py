import typing

from pyneo4j_ogm import (  # type: ignore
    RelationshipProperty,
    RelationshipPropertyDirection,
    RelationshipPropertyCardinality,
)

from src.entities.base import BaseNode
from src.relationships.default import Default


if typing.TYPE_CHECKING:
    from src.entities.scope.models import Scope  # noqa
    from src.entities.user.models import User  # noqa


class Resource(BaseNode):
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

    @property
    def type(self):
        return self.attr

    @type.setter
    def type(self, value):
        self.attr = value
