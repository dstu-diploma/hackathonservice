from fastapi import APIRouter
from .hackathon import router as hackathon_router
from .teams import router as teams_router
from .criterion import router as criterion_router

router = APIRouter(prefix="/manage")
router.include_router(hackathon_router)
router.include_router(teams_router)
router.include_router(criterion_router)
