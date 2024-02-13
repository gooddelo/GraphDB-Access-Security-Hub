import aiofiles


class ConfigDAO:
    config: dict = {}

    @classmethod
    async def load(cls):
        async with aiofiles.open("filename", mode="r") as config_file:
            ...
