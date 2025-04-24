from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_hackathon_t_team_id_b293f4";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_hackathon_t_hackath_3d8287" ON "hackathon_teams" ("hackathon_id", "team_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX IF EXISTS "uid_hackathon_t_hackath_3d8287";
        CREATE UNIQUE INDEX IF NOT EXISTS "uid_hackathon_t_team_id_b293f4" ON "hackathon_teams" ("team_id");"""
