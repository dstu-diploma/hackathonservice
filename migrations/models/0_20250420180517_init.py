from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "hackathons" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(40) NOT NULL UNIQUE,
    "start_date" TIMESTAMPTZ NOT NULL,
    "end_date" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "hackathon_teams" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "team_id" INT NOT NULL UNIQUE,
    "hackathon_id" INT NOT NULL REFERENCES "hackathons" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
