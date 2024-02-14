from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
import aiofiles

from src.entities.config.dal import ConfigDAO, CONFIG_PATH
from src.entities.config.dto import ConditionsDTO
from src.entities.config.exceptions import (
    SubjectRoleNotConfiguredError,
    ActionNotAllowedError,
)


@asynccontextmanager
async def mock_open(filename, mode="r"):
    class MockFile:
        async def read(self):
            return """
        owner:
            test_resource:
                create:
                delete:
                    max_depth: 1
        """

    if filename == CONFIG_PATH:
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
            "owner": {
                "test_resource": {"create": None, "delete": ConditionsDTO(max_depth=1)}
            }
        }

    async def test_get_permit_conditions_none(self):
        await ConfigDAO.load()
        assert (
            await ConfigDAO.get_permit_conditions("owner", "test_resource", "create")
            is None
        )

    async def test_get_permit_conditions_depth(self):
        await ConfigDAO.load()
        assert await ConfigDAO.get_permit_conditions(
            "owner", "test_resource", "delete"
        ) == ConditionsDTO(max_depth=1)

    async def test_get_permit_conditions_role_not_in_config(self):
        await ConfigDAO.load()
        with pytest.raises(SubjectRoleNotConfiguredError, match="not_exist"):
            await ConfigDAO.get_permit_conditions(
                "not_exist", "test_resource", "create"
            )

    async def test_get_permit_conditions_type_not_in_config(self):
        await ConfigDAO.load()
        with pytest.raises(ActionNotAllowedError, match="owner\tnot_exist\tcreate"):
            await ConfigDAO.get_permit_conditions("owner", "not_exist", "create")

    async def test_get_permit_conditions_action_not_in_config(self):
        await ConfigDAO.load()
        with pytest.raises(
            ActionNotAllowedError, match="owner\ttest_resource\tnot_exist"
        ):
            await ConfigDAO.get_permit_conditions("owner", "test_resource", "not_exist")
