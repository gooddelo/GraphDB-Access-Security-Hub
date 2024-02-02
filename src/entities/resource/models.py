import uuid

from pyneo4j_ogm import NodeModel  # type: ignore


class Resource(NodeModel):
    id: uuid.UUID
    type: str
