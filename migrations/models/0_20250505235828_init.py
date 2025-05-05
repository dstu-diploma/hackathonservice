from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "hackathons" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(40) NOT NULL UNIQUE,
    "description" VARCHAR(2000) NOT NULL DEFAULT '',
    "max_participant_count" INT NOT NULL,
    "max_team_mates_count" INT NOT NULL,
    "start_date" TIMESTAMPTZ NOT NULL,
    "score_start_date" TIMESTAMPTZ NOT NULL,
    "end_date" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "hackathon_criteria" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "weight" DOUBLE PRECISION NOT NULL,
    "hackathon_id" INT NOT NULL REFERENCES "hackathons" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_hackathon_c_hackath_60e116" UNIQUE ("hackathon_id", "name")
);
CREATE TABLE IF NOT EXISTS "hackathon_judges" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "hackathon_id" INT NOT NULL REFERENCES "hackathons" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_hackathon_j_hackath_5d7e29" UNIQUE ("hackathon_id", "user_id")
);
CREATE TABLE IF NOT EXISTS "team_scores" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "team_id" INT NOT NULL,
    "score" INT NOT NULL,
    "criterion_id" INT NOT NULL REFERENCES "hackathon_criteria" ("id") ON DELETE CASCADE,
    "judge_id" INT NOT NULL REFERENCES "hackathon_judges" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_team_scores_team_id_27ddfb" UNIQUE ("team_id", "criterion_id", "judge_id")
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
