from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "team_submissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "team_id" INT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "s3_key" VARCHAR(1024) NOT NULL,
    "content_type" VARCHAR(255) NOT NULL,
    "uploaded_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "hackathon_id" INT NOT NULL REFERENCES "hackathons" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_team_submis_team_id_49012d" UNIQUE ("team_id", "hackathon_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "team_submissions";"""
