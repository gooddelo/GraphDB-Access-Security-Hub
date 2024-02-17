from contextlib import asynccontextmanager

import aiofiles
import pytest_asyncio

from src.entities.config.dal import CONFIG_PATH


@asynccontextmanager
async def mock_open_small_config(filename, mode="r"):
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

    if filename == CONFIG_PATH:
        yield MockFile()
    else:
        raise FileNotFoundError()


@asynccontextmanager
async def mock_open_big_config(filename, mode="r"):
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

    if filename == CONFIG_PATH:
        yield MockFile()
    else:
        raise FileNotFoundError()


@pytest_asyncio.fixture
async def patch_open_small_config(monkeypatch):
    monkeypatch.setattr(aiofiles, "open", mock_open_small_config)


@pytest_asyncio.fixture
async def patch_open_big_config(monkeypatch):
    monkeypatch.setattr(aiofiles, "open", mock_open_big_config)
