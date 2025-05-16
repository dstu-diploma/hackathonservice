from zipfile import ZipFile
import mimetypes
import io

mimetypes.add_type(
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".docx",
)
mimetypes.add_type("application/msword", ".doc")
mimetypes.add_type(
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".pptx",
)
mimetypes.add_type("application/vnd.ms-powerpoint", ".ppt")


def is_valid_docx(bytes: io.BytesIO) -> bool:
    try:
        with ZipFile(bytes) as file:
            if (
                "[Content_Types].xml" not in file.namelist()
                or "word/document.xml" not in file.namelist()
            ):
                return False
        return True
    except Exception:
        return False


def is_valid_pptx(bytes: io.BytesIO) -> bool:
    try:
        with ZipFile(bytes) as file:
            if (
                "[Content_Types].xml" not in file.namelist()
                or "ppt/presentation.xml" not in file.namelist()
            ):
                return False
        return True
    except Exception:
        return False


def guess_content_type(filename: str) -> str:
    content_type, _ = mimetypes.guess_type(filename)
    if content_type is None:
        return "application/octet-stream"
    return content_type
