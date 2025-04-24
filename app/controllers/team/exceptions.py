from fastapi import HTTPException


class TeamServiceError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Произошла ошибка при обращении к сервису команд!",
        )
