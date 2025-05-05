from fastapi import HTTPException


class NoSuchHackathonException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404, detail="Хакатона с таким ID не существует!"
        )


class HackathonNameIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Данное имя занято!")


class HackathonValidationErrorException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class HackathonCriteriaNameIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Данное название критерия занято!"
        )


class HackathonCriteriaNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Такого критерия не существует!"
        )


class HackathonCriteriaValidationErrorException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
