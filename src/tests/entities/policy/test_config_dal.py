import pytest
import pytest_asyncio

from src.entities.policy.dal import PolicyDAO
from src.entities.policy.dto import ConditionsDTO
from src.entities.policy.exceptions import (
    SubjectRoleNotConfiguredError,
    ActionNotAllowedError,
)


@pytest.mark.asyncio
class TestPolicyDAL:
    @pytest_asyncio.fixture(autouse=True)
    async def patch_open(self, patch_open_small_policy):
        yield

    async def test_load_policy(self):
        await PolicyDAO.load()
        assert PolicyDAO.policy == {
            "owner": {
                "test_resource": {
                    "create": ConditionsDTO(),
                    "delete": ConditionsDTO(max_depth=1),
                },
                "test_resource_2": {
                    "create": ConditionsDTO(),
                    "update": ConditionsDTO(max_depth=1),
                },
            }
        }

    async def test_get_permit_conditions_none(self):
        await PolicyDAO.load()
        assert (
            await PolicyDAO.get_permit_conditions("owner", "test_resource", "create")
            == ConditionsDTO()
        )

    async def test_get_permit_conditions_depth(self):
        await PolicyDAO.load()
        assert await PolicyDAO.get_permit_conditions(
            "owner", "test_resource", "delete"
        ) == ConditionsDTO(max_depth=1)

    async def test_get_permit_conditions_role_not_in_policy(self):
        await PolicyDAO.load()
        with pytest.raises(SubjectRoleNotConfiguredError, match="not_exist"):
            await PolicyDAO.get_permit_conditions(
                "not_exist", "test_resource", "create"
            )

    async def test_get_permit_conditions_type_not_in_policy(self):
        await PolicyDAO.load()
        with pytest.raises(
            ActionNotAllowedError, match="Subj: owner; Obj: not_exist; Act: create;"
        ):
            await PolicyDAO.get_permit_conditions("owner", "not_exist", "create")

    async def test_get_permit_conditions_action_not_in_policy(self):
        await PolicyDAO.load()
        with pytest.raises(
            ActionNotAllowedError,
            match="Subj: owner; Obj: test_resource; Act: not_exist;",
        ):
            await PolicyDAO.get_permit_conditions("owner", "test_resource", "not_exist")
