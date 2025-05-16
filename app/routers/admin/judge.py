from app.services.judge.interface import IJudgeService
from app.routers.admin.dto import JudgeUserIdDto
from app.dependencies import get_judge_service
from app.services.auth import PermittedAction
from app.services.judge.dto import JudgeDto
from app.acl.permissions import Permissions
from fastapi import APIRouter, Depends

router = APIRouter(tags=["Управление жюри"], prefix="/judge")


@router.get(
    "/{hackathon_id}", response_model=list[JudgeDto], summary="Список судей"
)
async def get_judges(
    hackathon_id: int,
    _=Depends(PermittedAction(Permissions.GetJudges)),
    judge_service: IJudgeService = Depends(get_judge_service),
):
    """
    Возвращает список всех жюри для данного хакатона.
    """
    return await judge_service.get_judges(hackathon_id)


@router.post(
    "/{hackathon_id}", response_model=JudgeDto, summary="Добавление судьи"
)
async def add_judge(
    hackathon_id: int,
    dto: JudgeUserIdDto,
    _=Depends(PermittedAction(Permissions.CreateJudge)),
    judge_service: IJudgeService = Depends(get_judge_service),
):
    """
    Добавляет нового жюри на хакатон. Менять состав судей можно только до начала даты оценивания.
    """
    return await judge_service.add_judge(hackathon_id, dto.judge_user_id)


@router.delete(
    "/{hackathon_id}", response_model=JudgeDto, summary="Удаление судьи"
)
async def delete_judge(
    hackathon_id: int,
    dto: JudgeUserIdDto,
    _=Depends(PermittedAction(Permissions.DeleteJudge)),
    judge_service: IJudgeService = Depends(get_judge_service),
):
    """
    Удаляет жюри из списка для данного хакатона. Менять состав судей можно только до начала даты оценивания.
    """
    return await judge_service.delete_judge(hackathon_id, dto.judge_user_id)
