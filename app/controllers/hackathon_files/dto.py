from datetime import datetime
from pydantic import BaseModel

from app.models.hackathon import HackathonDocumentModel


class HackathonDocumentDto(BaseModel):
    id: int
    hackathon_id: int
    name: str
    content_type: str
    uploaded_at: datetime

    @staticmethod
    def from_tortoise(document: HackathonDocumentModel):
        return HackathonDocumentDto(
            id=document.id,
            hackathon_id=document.hackathon_id,  # type: ignore[attr-defined]
            name=document.name,
            content_type=document.content_type,
            uploaded_at=document.uploaded_at,
        )


class HackathonDocumentWithLinkDto(HackathonDocumentDto):
    link: str
