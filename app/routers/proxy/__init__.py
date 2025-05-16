from app.routers.proxy.exceptions import HackathonTeamSubmissionAccessError
from app.services.hackathon_files.interface import IHackathonFilesService
from app.dependencies import get_hackathon_files_service, get_storage
from app.ports.storage import IStoragePort
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends
import botocore.exceptions

router = APIRouter(prefix="/download", include_in_schema=False)


@router.get("/hack/{document_id}/{filename}")
async def download_hack_document(
    document_id: int,
    filename: str,
    hackathon_files_service: IHackathonFilesService = Depends(
        get_hackathon_files_service
    ),
    s3_service: IStoragePort = Depends(get_storage),
):
    s3_key = await hackathon_files_service.get_doc_s3_key(document_id)
    try:
        s3_obj = s3_service.get_object("hackathons", s3_key)

        return StreamingResponse(
            s3_obj["Body"],
            media_type=s3_obj["ContentType"],
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            },
        )
    except botocore.exceptions.ClientError:
        raise HackathonTeamSubmissionAccessError
