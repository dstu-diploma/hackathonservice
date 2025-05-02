from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "hackathon_teams";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
