from pathlib import Path

from typing import Dict

import aiofiles
import yaml

from src.entities.config.dto import ConditionsDTO
from src.entities.config.exceptions import (
    SubjectRoleNotConfiguredError,
    ActionNotAllowedError,
)

CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "config" / "config.yml"


class ConfigDAO:
    config: Dict[str, Dict[str, Dict[str, ConditionsDTO | None]]] = {}

    @classmethod
    async def load(cls):
        async with aiofiles.open(CONFIG_PATH, mode="r") as config_file:
            config_str = await config_file.read()
            config_dict = yaml.safe_load(config_str)
            for role in config_dict.keys():
                for object in config_dict[role].keys():
                    cls.config[role] = dict.fromkeys(config_dict[role].keys(), None)
                    for action in config_dict[role][object].keys():
                        cls.config[role][object] = dict.fromkeys(
                            config_dict[role][object].keys(), None
                        )
                        conditions = config_dict[role][object][action]
                        if conditions is not None:
                            cls.config[role][object][action] = ConditionsDTO(
                                **conditions
                            )

    @classmethod
    async def get_permit_conditions(
        cls, role: str, object: str, action: str
    ) -> ConditionsDTO | None:
        try:
            return cls.config[role][object][action]
        except KeyError:
            try:
                cls.config[role]
            except KeyError:
                raise SubjectRoleNotConfiguredError(role)
            else:
                raise ActionNotAllowedError(f"{role}\t{object}\t{action}")
