from app.ports.storage import IStoragePort
from typing import Protocol
import io

from app.services.hackathon_files.dto import (
    HackathonDocumentDto,
    HackathonDocumentWithLinkDto,
)


class IHackathonFilesService(Protocol):
    bucket: str
    storage: IStoragePort

    async def upload_allowed_file(
        self, hackathon_id: int, file: io.BytesIO, filename: str
    ) -> HackathonDocumentDto: ...
    def is_allowed_file(
        self, filename: str, file_bytes: io.BytesIO
    ) -> bool: ...
    async def get_files(
        self, hackathon_id: int, base_url: str
    ) -> list[HackathonDocumentWithLinkDto]: ...
    async def get_doc_s3_key(self, document_id: int) -> str: ...
    async def generate_redirect_link(
        self, base_url: str, filename: str, document_id: int
    ) -> str: ...
    async def delete_file(self, document_id: int) -> HackathonDocumentDto: ...
