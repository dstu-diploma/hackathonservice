from app.controllers.hackathon import (
    get_hackathon_controller,
    HackathonController,
)
from fastapi import APIRouter, Depends

router = APIRouter(tags=["Основное"], prefix="")


@router.get("/")
async def get_all(
    hackathon_controller: HackathonController = Depends(
        get_hackathon_controller
    ),
):
    return await hackathon_controller.get_all()
