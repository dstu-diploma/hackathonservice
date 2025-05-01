from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "hackathons" ADD "score_start_date" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "hackathon_teams" ADD "score" INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "hackathons" DROP COLUMN "score_start_date";
        ALTER TABLE "hackathon_teams" DROP COLUMN "score";"""
