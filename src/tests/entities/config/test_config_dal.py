from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
import aiofiles

from src.entities.config.dal import ConfigDAO, CONFIG_FILENAME
from src.entities.config.dto import ConditionsDTO


@asynccontextmanager
async def mock_open(filename, mode="r"):
    class MockFile:
        async def read(self):
            return """
        owner:
            test_resource:
                create:
                delete:
                    depth: 1
        """

    if filename == CONFIG_FILENAME:
        yield MockFile()
    else:
        raise FileNotFoundError()


@pytest.mark.asyncio
class TestConfigDAL:
    @pytest_asyncio.fixture(autouse=True)
    async def patch_open(self, monkeypatch):
        monkeypatch.setattr(aiofiles, "open", mock_open)

    async def test_load_config(self):
        await ConfigDAO.load()
        assert ConfigDAO.config == {
            "owner": {"test_resource": {"create": None, "delete": ConditionsDTO(depth=1)}}
        }
    
    async def test_get_permit_conditions_none(self):
        await ConfigDAO.load()
        assert await ConfigDAO.get_permit_conditions("owner", "test_resource", "create") is None
                
    async def test_get_permit_conditions_depth(self):
        await ConfigDAO.load()
        assert await ConfigDAO.get_permit_conditions("owner", "test_resource", "delete") == ConditionsDTO(depth=1)

    async def test_get_permit_conditions_role_not_exist(self):
        await ConfigDAO.load()
        with pytest.raises(KeyError):
            await ConfigDAO.get_permit_conditions("not_exist", "test_resource", "create")
                
                