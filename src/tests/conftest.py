import asyncio
import uuid
from contextlib import asynccontextmanager

import aiofiles
import pytest
import pytest_asyncio
from _pytest.fixtures import SubRequest
from pyneo4j_ogm import Pyneo4jClient  # type: ignore
from testcontainers.neo4j import Neo4jContainer  # type: ignore

from src.entities.policy.dal import POLICY_PATH
from src.entities.user.models import User
from src.entities.resource.models import Resource
from src.entities.scope.models import Scope
from src.relationships.default import Default


@asynccontextmanager
async def mock_open_small_policy(filename, mode="r"):
    class MockFile:
        async def read(self):
            return """
        owner:
            test_resource:
                create:
                delete:
                    max_depth: 1
            test_resource_2:
                create:
                update:
                    max_depth: 1
        """

    if filename == POLICY_PATH:
        yield MockFile()
    else:
        raise FileNotFoundError()


@asynccontextmanager
async def mock_open_big_policy(filename, mode="r"):
    class MockFile:
        async def read(self):
            return """
        owner:
            self:
                create_company:
                create_personal_resource:
                read:
                update:
                delete:
            company_resource:
                read:
                update:
                delete:
            selling_point_resource:
                read:
                delete:
            personal_resource:
                read:
                update:
                    max_depth: 1
                delete:
                    max_depth: 1
            company:
                create_resource:
                create_employee:
                create_selling_point:
                read:
                update:
                delete:
            selling_point:
                create_resource:
                read:
                update:
                delete:
            employee:
                read:
                delete:
        employee:
            self:
                create_personal_resource:
                read:
                update:
                delete:
            personal_resource:
                read:
                update:
                    max_depth: 1
                delete:
                    max_depth: 1
            selling_point:
                create_resource:
                read:
            selling_point_resource:
                read:
                update:
            employee:
                read:
        """

    if filename == POLICY_PATH:
        yield MockFile()
    else:
        raise FileNotFoundError()


@pytest_asyncio.fixture
async def patch_open_small_policy(monkeypatch):
    monkeypatch.setattr(aiofiles, "open", mock_open_small_policy)


@pytest_asyncio.fixture
async def patch_open_big_policy(monkeypatch):
    monkeypatch.setattr(aiofiles, "open", mock_open_big_policy)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def neo4j_client():
    with Neo4jContainer() as neo4j:
        url = neo4j.get_connection_url()
        client = Pyneo4jClient()
        await client.connect(uri=url, auth=("neo4j", "password"), database="neo4j")
        await client.register_models([User, Resource, Scope, Default])
        yield client
        await client.close()


@pytest_asyncio.fixture
async def drop_nodes(neo4j_client: Pyneo4jClient):
    await neo4j_client.drop_nodes()
    yield


@pytest_asyncio.fixture
async def user_nodes(request: SubRequest):
    users_data = request.param
    users = []
    if len(users_data) > 0:
        if isinstance(users_data[0], uuid.UUID):
            users = [
                await User(user_id=user_id, role="user").create()
                for user_id in users_data
            ]
        elif isinstance(users_data[0], tuple):
            users = [
                await User(user_id=user_id, role=role).create()
                for user_id, role in users_data
            ]
    return users


@pytest_asyncio.fixture
async def scope_nodes(request: SubRequest):
    scopes_data = request.param
    scopes = []
    if len(scopes_data) > 0:
        if isinstance(scopes_data[0], uuid.UUID):
            scopes = [
                await Scope(scope_id=scope_id, name="company").create()
                for scope_id in scopes_data
            ]
        elif isinstance(scopes_data[0], tuple):
            scopes = [
                await Scope(scope_id=scope_id, name=name).create()
                for scope_id, name in scopes_data
            ]
    return scopes


@pytest_asyncio.fixture
async def resource_nodes(request: SubRequest):
    resources_data = request.param
    resources = []
    if len(resources_data) > 0:
        if isinstance(resources_data[0], uuid.UUID):
            resources = [
                await Resource(resource_id=resource_id, type="resource").create()
                for resource_id in resources_data
            ]
        elif isinstance(resources_data[0], tuple):
            resources = [
                await Resource(resource_id=resource_id, type=type).create()
                for resource_id, type in resources_data
            ]
    return resources
