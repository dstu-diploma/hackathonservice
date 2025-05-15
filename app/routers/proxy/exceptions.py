from fastapi import HTTPException


class HackathonTeamNoSubmissionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Данная команда не загружала файлы!",
        )
