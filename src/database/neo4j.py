from pyneo4j_ogm import Pyneo4jClient  # type: ignore

from src.relationships import Default
from src.entities.user.models import User
from src.entities.scope.models import Scope
from src.entities.resource.models import Resource
from src.config.neo4j import NEO4J_CONFIG


CLIENT = Pyneo4jClient()


async def init_client():
    print()
    await CLIENT.connect(
        uri=NEO4J_CONFIG.connection_string,
        auth=(NEO4J_CONFIG.user, NEO4J_CONFIG.password),
        database=NEO4J_CONFIG.db,
    )
    await CLIENT.register_models([User, Resource, Scope, Default])


async def close_client():
    await CLIENT.close()
