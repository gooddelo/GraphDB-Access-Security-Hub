import pytest_asyncio

from src.entities.policy.dal import PolicyDAO
from src.api.amqp.main import broker, api_router


@pytest_asyncio.fixture(autouse=True)
async def drop_nodes_(drop_nodes):
    yield


@pytest_asyncio.fixture(scope="session", autouse=True)
async def neo4j_client_(neo4j_client):
    yield


@pytest_asyncio.fixture(autouse=True)
async def set_policy(patch_open_big_policy):
    await PolicyDAO.load()
    yield
    PolicyDAO.policy = {}


@pytest_asyncio.fixture(scope="session", autouse=True)
async def set_routers():
    broker.include_routers(api_router)
