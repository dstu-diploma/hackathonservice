from app.controllers.judge import IJudgeController, get_judge_controller
from app.controllers.auth import PermittedAction
from app.controllers.judge.dto import JudgeDto
from app.acl.permissions import Permissions
from fastapi import APIRouter, Depends

from app.views.admin.dto import JudgeUserIdDto

router = APIRouter(tags=["Управление жюри"], prefix="/judge")


@router.get(
    "/{hackathon_id}", response_model=list[JudgeDto], summary="Список судей"
)
async def get_judges(
    hackathon_id: int,
    _=Depends(PermittedAction(Permissions.GetJudges)),
    judge_controller: IJudgeController = Depends(get_judge_controller),
):
    """
    Возвращает список всех жюри для данного хакатона.
    """
    return await judge_controller.get_judges(hackathon_id)


@router.post(
    "/{hackathon_id}", response_model=JudgeDto, summary="Добавление судьи"
)
async def add_judge(
    hackathon_id: int,
    dto: JudgeUserIdDto,
    _=Depends(PermittedAction(Permissions.CreateJudge)),
    judge_controller: IJudgeController = Depends(get_judge_controller),
):
    """
    Добавляет нового жюри на хакатон. Менять состав судей можно только до начала даты оценивания.
    """
    return await judge_controller.add_judge(hackathon_id, dto.judge_user_id)


@router.delete(
    "/{hackathon_id}", response_model=JudgeDto, summary="Удаление судьи"
)
async def delete_judge(
    hackathon_id: int,
    dto: JudgeUserIdDto,
    _=Depends(PermittedAction(Permissions.DeleteJudge)),
    judge_controller: IJudgeController = Depends(get_judge_controller),
):
    """
    Удаляет жюри из списка для данного хакатона. Менять состав судей можно только до начала даты оценивания.
    """
    return await judge_controller.delete_judge(hackathon_id, dto.judge_user_id)
