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
            detail="У данного хакатона истек срок, в течение которого можно было ставить оценки!",
        )


class HackathonTeamCantGetResultsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Для данного хакатона еще не наступил срок, когда можно смотреть результаты!",
        )


class HackathonTeamCantUploadSubmissionsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Загружать результаты можно только до начала критериев оценивания!",
        )
