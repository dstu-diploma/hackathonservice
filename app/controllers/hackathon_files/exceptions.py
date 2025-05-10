from fastapi import HTTPException


class HackathonFileTypeRestrictedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Данный тип файла запрещен к загрузке!",
        )


class HackathonFileNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Этого файла не существует!",
        )
