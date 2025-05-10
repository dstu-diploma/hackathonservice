from app.controllers.s3 import IS3Controller, get_s3_controller
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends

from app.controllers.hackathon_files import (
    IHackathonFilesController,
    get_hackathon_files_controller,
)

router = APIRouter(prefix="/download", include_in_schema=False)


@router.get("/{document_id}/{filename}")
async def download_document(
    document_id: int,
    filename: str,
    hackathon_files_controller: IHackathonFilesController = Depends(
        get_hackathon_files_controller
    ),
    s3_controller: IS3Controller = Depends(get_s3_controller),
):
    s3_key = await hackathon_files_controller.get_doc_s3_key(document_id)
    s3_obj = s3_controller.get_object("hackathons", s3_key)

    return StreamingResponse(
        s3_obj["Body"],
        media_type=s3_obj["ContentType"],
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
