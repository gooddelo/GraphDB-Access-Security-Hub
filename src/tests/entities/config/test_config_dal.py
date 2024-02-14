from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
import aiofiles

from src.entities.config.dal import ConfigDAO, CONFIG_FILENAME

@asynccontextmanager
async def mock_open(filename, mode="r"):
    if filename == CONFIG_FILENAME:
        yield """
        owner:
            test_owner
        """
    else:
        raise FileNotFoundError()


@pytest.mark.asyncio
class TestConfigDAL:
    @pytest_asyncio.fixture(autouse=True)
    async def patch_open(self, monkeypatch):
        monkeypatch.setattr(aiofiles, "open", mock_open)

    async def test_load_config(self):
        await ConfigDAO.load()
        assert ConfigDAO.config == {"owner": "test_owner"}
