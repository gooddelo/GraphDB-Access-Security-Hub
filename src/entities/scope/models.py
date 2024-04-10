from pydantic import Field
from pyneo4j_ogm import (  # type: ignore
    RelationshipProperty,
    RelationshipPropertyDirection,
    RelationshipPropertyCardinality,
)

from src.entities.scope.exceptions import (
    ScopeNotFoundException,
    ScopeAlreadyExistException,
)
from src.entities.policy.models import Policy
from src.entities.resource.models import Resource
from src.entities.user.models import User
from src.entities.base import BaseNode
from src.relationships import Default


class Scope(BaseNode):
    exists_exception = ScopeAlreadyExistException
    not_found_exception = ScopeNotFoundException

    policy: Policy = Field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.attr

    @name.setter
    def name(self, value: str):
        self.attr = value

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
        direction=RelationshipPropertyDirection.INCOMING,
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
