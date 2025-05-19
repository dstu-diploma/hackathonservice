from app.services.hackathon_files.interface import IHackathonFilesService
from app.models import HackathonModel, HackathonDocumentModel
from app.ports.storage import IStoragePort
from urllib.parse import quote
from uuid import uuid4
from . import utils
import urllib.parse
import mimetypes
import io


from app.services.hackathon_files.dto import (
    HackathonDocumentDto,
    HackathonDocumentWithLinkDto,
)
from app.services.hackathon_files.exceptions import (
    HackathonFileNotFoundException,
    HackathonFileTypeRestrictedException,
)


class HackathonFilesService(IHackathonFilesService):
    def __init__(self, bucket: str, storage: IStoragePort):
        self.bucket = bucket
        self.storage = storage

    async def upload_allowed_file(
        self, hackathon_id: int, file: io.BytesIO, filename: str
    ) -> HackathonDocumentDto:
        file.seek(0)

        if not self.is_allowed_file(filename, file):
            raise HackathonFileTypeRestrictedException()

        return await self._upload_and_save(hackathon_id, file, filename)

    def is_allowed_file(self, filename: str, file_bytes: io.BytesIO) -> bool:

        mime_type, _ = mimetypes.guess_type(filename)

        if mime_type is None:
            mime_type = self._get_mime_type_from_content(file_bytes)

        allowed_mime_types = [
            "application/msword",  # .doc
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
            "application/vnd.ms-powerpoint",  # .ppt
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # .pptx
            "text/plain",  # .txt
            "image/jpeg",  # jpg/jpeg
            "image/png",  # png
        ]

        return mime_type in allowed_mime_types

    def _get_mime_type_from_content(self, file_bytes: io.BytesIO) -> str:
        file_bytes.seek(0)

        try:
            if utils.is_valid_docx(file_bytes):
                return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if utils.is_valid_pptx(file_bytes):
                return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        except Exception:
            pass

        return "unknown"

    async def _upload_and_save(
        self, hackathon_id: int, file: io.BytesIO, filename: str
    ) -> HackathonDocumentDto:
        hackathon = await HackathonModel.get(id=hackathon_id)
        content_type = utils.guess_content_type(filename)
        key = f"organizer_uploads/{hackathon_id}/{uuid4()}_{filename}"

        file.seek(0)
        self.storage.upload_file(
            file, bucket=self.bucket, key=key, content_type=content_type
        )

        document = await HackathonDocumentModel.create(
            hackathon=hackathon,
            name=filename,
            s3_key=key,
            content_type=content_type,
        )

        return HackathonDocumentDto.from_tortoise(document)

    async def get_files(
        self, hackathon_id: int, base_url: str
    ) -> list[HackathonDocumentWithLinkDto]:
        docs = await HackathonDocumentModel.filter(
            hackathon_id=hackathon_id
        ).all()

        result: list[HackathonDocumentWithLinkDto] = []

        for doc in docs:
            doc_dto = HackathonDocumentDto.from_tortoise(doc)

            result.append(
                HackathonDocumentWithLinkDto(
                    link=await self.generate_redirect_link(
                        base_url, doc.name, doc.id
                    ),
                    **doc_dto.model_dump(),
                )
            )

        return result

    async def _get_document(self, document_id: int) -> HackathonDocumentModel:
        doc = await HackathonDocumentModel.get_or_none(id=document_id)
        if doc is None:
            raise HackathonFileNotFoundException()

        return doc

    async def get_doc_s3_key(self, document_id: int) -> str:
        doc = await self._get_document(document_id)
        return doc.s3_key

    async def generate_redirect_link(
        self, base_url: str, filename: str, document_id: int
    ) -> str:
        doc = await self._get_document(document_id)

        safe_filename = quote(filename)
        redirect_url = urllib.parse.urljoin(
            base_url, f"download/hack/{doc.id}/{safe_filename}"
        )
        return redirect_url

    async def delete_file(self, document_id: int) -> HackathonDocumentDto:
        doc = await HackathonDocumentModel.get_or_none(id=document_id)
        if not doc:
            raise HackathonFileNotFoundException()

        self.storage.delete_object(bucket=self.bucket, key=doc.s3_key)
        await doc.delete()
        return HackathonDocumentDto.from_tortoise(doc)
