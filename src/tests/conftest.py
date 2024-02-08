import asyncio
from typing import Iterator

import pytest
import pytest_asyncio
from _pytest.fixtures import SubRequest
from pyneo4j_ogm import Pyneo4jClient  # type: ignore
from testcontainers.neo4j import Neo4jContainer  # type: ignore

from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.scope.models import Scope
from src.relationships.default import Default


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
        await client.register_models([User, Resource, Scope, Default])
        yield client
        await client.close()


@pytest_asyncio.fixture(autouse=True)
async def drop_nodes(neo4j_client: Pyneo4jClient):
    await neo4j_client.drop_nodes()
    yield


@pytest_asyncio.fixture
async def user_nodes(request: SubRequest):
    user_ids = request.param
    users = [await User(user_id=user_id, role="user").create() for user_id in user_ids]
    return users


@pytest_asyncio.fixture
async def scope_nodes(request: SubRequest):
    scope_ids = request.param
    scopes = [
        await Scope(scope_id=scope_id, name="company").create()
        for scope_id in scope_ids
    ]
    return scopes


@pytest_asyncio.fixture
async def resource_nodes(request: SubRequest):
    resource_ids = request.param
    resources = [
        await Resource(resource_id=resource_id, type="resource").create()
        for resource_id in resource_ids
    ]
    return resources
