from fastapi import HTTPException


class HackathonJudgeDoesNotExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Пользователь с данным ID не принадлежит к членам жюри этого хакатона!",
        )


class HackathonJudgeUnauthorizedRoleException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail='Членом жюри может являться только пользоваль с ролью "Судья"!',
        )


class HackathonJudgeAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Пользователь с данным ID и так принадлежит к членам жюри этого хакатона!",
        )


class HackathonJudgeCantManageDateExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Списком судей можно управлять только до начала хакатона!",
        )
