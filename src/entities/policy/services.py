from src.entities.policy.dal import PolicyDAO


async def init_policy():
    await PolicyDAO.load()
