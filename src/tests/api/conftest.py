import pytest_asyncio

from src.entities.policy.dal import PolicyDAO


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
