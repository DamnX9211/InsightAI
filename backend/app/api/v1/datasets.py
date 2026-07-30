from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.dataset_service import DatasetService
from app.database.dependencies import get_db
from app.schemas.dataset import DatasetResponse

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
)

@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(file: UploadFile, db: Session = Depends(get_db)):
    return await DatasetService.upload_dataset(file=file, db=db)