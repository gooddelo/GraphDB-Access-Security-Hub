from pathlib import Path

import aiofiles
import yaml

CONFIG_FILENAME = Path(__file__).parent.parent.parent.parent / 'config' / 'config.yml'


class ConfigDAO:
    config: dict = {}

    @classmethod
    async def load(cls):
        async with aiofiles.open(CONFIG_FILENAME, mode="r") as config_file:
            config_dict = await config_file.read()
            cls.config = yaml.safe_load(config_dict)
