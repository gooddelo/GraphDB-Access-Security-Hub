from pathlib import Path

from typing import Dict

import aiofiles
import yaml

from src.entities.policy.dto import ConditionsDTO
from src.entities.policy.exceptions import (
    RoleNotConfiguredError,
    ActionNotConfiguredError,
)

POLICY_PATH = Path(__file__).parent.parent.parent.parent / "policy" / "policy.yml"


class PolicyDAO:
    policy: Dict[str, Dict[str, Dict[str, ConditionsDTO]]] = {}

    @classmethod
    async def load(cls):
        async with aiofiles.open(POLICY_PATH, mode="r") as policy_file:
            policy_str = await policy_file.read()
            policy_dict = yaml.safe_load(policy_str)
            for role in policy_dict.keys():
                cls.policy[role] = dict.fromkeys(policy_dict[role].keys(), {})
                for object in policy_dict[role].keys():
                    cls.policy[role][object] = dict.fromkeys(
                        policy_dict[role][object].keys(), {}
                    )
                    for action in policy_dict[role][object].keys():
                        conditions = policy_dict[role][object][action]
                        try:
                            cls.policy[role][object][action] = ConditionsDTO(
                                **conditions
                            )
                        except TypeError:
                            cls.policy[role][object][action] = ConditionsDTO()

    @classmethod
    async def get_permit_conditions(
        cls, role: str, object: str, action: str
    ) -> ConditionsDTO:
        try:
            return cls.policy[role][object][action]
        except KeyError:
            try:
                cls.policy[role]
            except KeyError:
                raise RoleNotConfiguredError(role)
            else:
                raise ActionNotConfiguredError(role, object, action)
