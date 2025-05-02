from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "hackathons" ADD "max_participant_count" INT NOT NULL;
        ALTER TABLE "hackathons" ADD "max_team_mates_count" INT NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "hackathons" DROP COLUMN "max_participant_count";
        ALTER TABLE "hackathons" DROP COLUMN "max_team_mates_count";"""
