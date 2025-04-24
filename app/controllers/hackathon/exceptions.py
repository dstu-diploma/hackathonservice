from fastapi import HTTPException


class NoSuchHackathonException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="No hackathon with such id!")


class HackathonNameIsNotUniqueException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="A hackathon with such name already exists!"
        )
