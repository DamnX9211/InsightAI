from pathlib import Path
import shutil
import uuid

from fastapi import HTTPException, UploadFile

from app.core.config import settings


UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class StorageService:

    ALLOWED_EXTENSIONS = {
        ".csv",
        ".xlsx",
        ".xls",
    }

    @staticmethod
    def save_uploaded_file(
        file: UploadFile,
    ) -> tuple[Path, int, str]:

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Filename missing.",
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in StorageService.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type.",
            )

        stored_filename = f"{uuid.uuid4()}{extension}"

        destination = UPLOAD_DIR / stored_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size = destination.stat().st_size

        return (
            destination,
            file_size,
            stored_filename,
        )