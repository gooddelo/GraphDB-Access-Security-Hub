import pytest
import pytest_asyncio
from pyneo4j_ogm import Pyneo4jClient  # type: ignore
from testcontainers.neo4j import Neo4jContainer  # type: ignore

from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.namespace.models import Namespace

url: str


@pytest.fixture(scope="session", autouse=True)
def neo4j_container():
    with Neo4jContainer() as neo4j:
        global url
        url = neo4j.get_connection_url()
        yield


@pytest_asyncio.fixture
async def neo4j_client():
    client = Pyneo4jClient()
    global url
    await client.connect(uri=url, auth=("neo4j", "password"), database="neo4j")
    await client.register_models([User, Resource, Namespace])
    yield client
    await client.close()
