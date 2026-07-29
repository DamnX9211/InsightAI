from fastapi import APIRouter, UploadFile

from app.services.dataset_service import DatasetService

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
)

@router.post("/upload")
async def upload_dataset(file: UploadFile):
    saved_path = await DatasetService.save_file(file)
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_to": str(saved_path)
    }