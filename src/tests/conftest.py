import asyncio
from typing import Iterator

import pytest
import pytest_asyncio
from pyneo4j_ogm import Pyneo4jClient  # type: ignore
from testcontainers.neo4j import Neo4jContainer  # type: ignore

from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.namespace.models import Namespace
from src.relationships.default import Default

url: str


@pytest.fixture(scope="session", autouse=True)
def event_loop(_session_event_loop) -> Iterator[asyncio.AbstractEventLoop]:
    yield _session_event_loop
    _session_event_loop.close()


@pytest_asyncio.fixture(scope="session")
async def neo4j_client():
    with Neo4jContainer() as neo4j:
        url = neo4j.get_connection_url()
        client = Pyneo4jClient()
        await client.connect(uri=url, auth=("neo4j", "password"), database="neo4j")
        await client.register_models([User, Resource, Namespace, Default])
        yield client
        await client.close()
    


@pytest_asyncio.fixture(autouse=True)
async def drop_nodes(neo4j_client: Pyneo4jClient):
    yield
    await neo4j_client.drop_nodes()