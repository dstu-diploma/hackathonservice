from fastapi import HTTPException


class TeamAlreadyParticipatingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Данная команда уже участвует в этом хакатоне!",
        )


class TeamIsNotParticipatingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Данная команда не является участником этого хакатона!",
        )
