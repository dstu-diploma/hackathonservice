import io
from os import environ
from uuid import uuid4
from app.controllers.hackathon_files import (
    IHackathonFilesController,
    get_hackathon_files_controller,
)
from app.controllers.hackathon_files.dto import (
    HackathonDocumentDto,
    HackathonDocumentWithLinkDto,
)
from app.views.admin.dto import CreateHackathonDto, HackathonFileIdDto
from app.controllers.auth import PermittedAction
from app.acl.permissions import Permissions
from fastapi import APIRouter, Depends, Request, UploadFile

from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)

from app.controllers.hackathon.dto import (
    OptionalHackathonDto,
    HackathonDto,
    TeamScoreDto,
)


router = APIRouter(tags=["Управление хакатонами"], prefix="/hackathon")
PUBLIC_API_URL = environ.get("PUBLIC_API_URL", None)


@router.post(
    "/",
    response_model=HackathonDto,
    summary="Создание хакатона",
)
async def create_hackathon(
    dto: CreateHackathonDto,
    _=Depends(PermittedAction(Permissions.CreateHackathon)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Регистрирует новый хакатон. Имя хакатона должно быть уникальным.
    """
    return await hackathon_controller.create(
        name=dto.name,
        max_participant_count=dto.max_participant_count,
        max_team_mates_count=dto.max_team_mates_count,
        description=dto.description,
        start_date=dto.start_date,
        score_start_date=dto.score_start_date,
        end_date=dto.end_date,
    )


@router.delete(
    "/{hackathon_id}",
    summary="Удаление хакатона",
)
async def delete_hackathon(
    hackathon_id: int,
    _=Depends(PermittedAction(Permissions.DeleteHackathon)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Полностью удаляет данные о хакатоне.
    """
    return await hackathon_controller.delete(hackathon_id)


@router.patch(
    "/{hackathon_id}",
    response_model=HackathonDto,
    summary="Обновление информации о хакатоне",
)
async def update_hackathon_data(
    hackathon_id: int,
    dto: OptionalHackathonDto,
    _=Depends(PermittedAction(Permissions.UpdateHackathon)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Позволяет обновить одно или несколько полей о хакатоне. Все поля необязательные.
    """
    return await hackathon_controller.update(hackathon_id, dto)


@router.put(
    "/{hackathon_id}/score",
    response_model=list[TeamScoreDto],
    summary="Рассчет результатов",
)
async def calculate_team_score(
    hackathon_id: int,
    _=Depends(PermittedAction(Permissions.ScoreHackathon)),
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    """
    Позволяет рассчитать оценки по результатам хакатона. Если оценивание уже проводилось, то оценки будут заменены.
    """
    scores = await hackathon_controller.calculate_team_scores_for_hackathon(
        hackathon_id, save_to_db=True
    )
    return scores


@router.get(
    "/{hackathon_id}/files",
    response_model=list[HackathonDocumentWithLinkDto],
    summary="Список вложений",
)
async def get_hackathon_files(
    hackathon_id: int,
    request: Request,
    _=Depends(PermittedAction(Permissions.ScoreHackathon)),
    hackathon_files_controller: IHackathonFilesController = Depends(
        get_hackathon_files_controller
    ),
):
    """
    Возвращает список всех загруженных файлов (приложений)
    """
    files = await hackathon_files_controller.get_files(
        hackathon_id, PUBLIC_API_URL or str(request.base_url).rstrip("/")
    )
    return files


@router.put(
    "/{hackathon_id}/files",
    response_model=HackathonDocumentDto,
    summary="Добавить файл",
)
async def add_hackathon_file(
    file: UploadFile,
    hackathon_id: int,
    _=Depends(PermittedAction(Permissions.UploadHackathonDocument)),
    hackathon_files_controller: IHackathonFilesController = Depends(
        get_hackathon_files_controller
    ),
):
    """
    Добавляет файл во вложения хакатона. Разрешенные форматы: doc, docx, ppt, pptx, txt
    """
    return await hackathon_files_controller.upload_allowed_file(
        hackathon_id,
        io.BytesIO(await file.read()),
        file.filename or str(uuid4()),
    )


@router.delete(
    "/{hackathon_id}/files",
    response_model=HackathonDocumentDto,
    summary="Удалить файл",
)
async def delete_hackathon_file(
    hackathon_id: int,
    dto: HackathonFileIdDto,
    _=Depends(PermittedAction(Permissions.DeleteHackathonDocument)),
    hackathon_files_controller: IHackathonFilesController = Depends(
        get_hackathon_files_controller
    ),
):
    """
    Удаляет файл из списка вложений.
    """
    return await hackathon_files_controller.delete_file(dto.file_id)
