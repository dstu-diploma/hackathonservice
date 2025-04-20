from fastapi import HTTPException


class NoSuchHackathonException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="No hackathon with such id!")
