import pytest_asyncio


@pytest_asyncio.fixture(autouse=True)
async def drop_nodes_(drop_nodes):
    yield
