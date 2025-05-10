from fastapi import HTTPException


class HackathonTeamAlreadyScoredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Судья уже давал данной команде оценку по этому критерию!",
        )


class HackathonTeamCantBeScoredDateExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Ставить оценки можно только от даты начала оценивания и до окончания хакатона!",
        )


class HackathonTeamCantGetResultsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Результаты хакатона можно смотреть только после его окончания!",
        )


class HackathonTeamCantUploadSubmissionsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Загружать результаты можно только до начала критериев оценивания!",
        )
