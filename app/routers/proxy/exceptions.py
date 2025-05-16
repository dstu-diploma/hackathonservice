from fastapi import HTTPException


class HackathonTeamNoSubmissionException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Данная команда не загружала файлы!",
        )


class HackathonTeamSubmissionAccessError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=501,
            detail="Произошла ошибка при попытке загрузить файл. Обратитесь в поддержку",
        )
