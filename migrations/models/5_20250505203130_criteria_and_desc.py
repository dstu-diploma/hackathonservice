from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "hackathon_criteria" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "weight" DOUBLE PRECISION NOT NULL,
    "hackathon_id" INT NOT NULL REFERENCES "hackathons" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_hackathon_c_hackath_60e116" UNIQUE ("hackathon_id", "name")
);
        ALTER TABLE "hackathons" ADD "description" VARCHAR(2000) NOT NULL DEFAULT '';
        CREATE TABLE IF NOT EXISTS "team_scores" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "team_id" INT NOT NULL,
    "score" INT NOT NULL,
    "criterion_id" INT NOT NULL REFERENCES "hackathon_criteria" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_team_scores_team_id_e67211" UNIQUE ("team_id", "criterion_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "hackathons" DROP COLUMN "description";
        DROP TABLE IF EXISTS "hackathon_criteria";
        DROP TABLE IF EXISTS "team_scores";"""
