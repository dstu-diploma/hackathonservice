from fastapi import HTTPException


class TeamAlreadyParticipatingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="The team is already participating in this hackathon!",
        )


class TeamIsNotParticipatingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="The team is not participating in this hackathon!",
        )
