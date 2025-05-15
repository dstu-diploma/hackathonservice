from app.services.s3 import IS3Service, get_s3_controller
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends

from app.services.hackathon_files import (
    IHackathonFilesService,
    get_hackathon_files_controller,
)

router = APIRouter(prefix="/download", include_in_schema=False)


@router.get("/hack/{document_id}/{filename}")
async def download_hack_document(
    document_id: int,
    filename: str,
    hackathon_files_controller: IHackathonFilesService = Depends(
        get_hackathon_files_controller
    ),
    s3_controller: IS3Service = Depends(get_s3_controller),
):
    s3_key = await hackathon_files_controller.get_doc_s3_key(document_id)
    s3_obj = s3_controller.get_object("hackathons", s3_key)

    return StreamingResponse(
        s3_obj["Body"],
        media_type=s3_obj["ContentType"],
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
