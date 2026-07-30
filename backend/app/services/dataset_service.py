from pathlib import Path
import shutil
import pandas as pd
from sqlalchemy.orm import Session
import uuid

from app.models.dataset import Dataset
from fastapi import UploadFile, HTTPException
from app.services.profiling_service import ProfilingService
from app.core.config import settings


UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

class DatasetService:
    @staticmethod
    async def upload_dataset(file: UploadFile, db: Session) -> dict:

 ## Validating Filename

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file must have a filename"
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid file type. Only CSV and Excel files are allowed.")


## generate unique stored name

        file_uuid = str(uuid.uuid4())
        stored_filename = f"{file_uuid}{extension}"

        destination = UPLOAD_DIR / stored_filename

## save uploaded file        
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

## validate file size

        file_size = destination.stat().st_size
        max_size_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

        if file_size > max_size_bytes:
            destination.unlink(missing_ok=True)
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds the {settings.MAX_UPLOAD_SIZE_MB} MB upload limit.",
            )    
## read dataset      
     
        try:
            if extension == ".csv":
                df = pd.read_csv(destination)
            else:
                df = pd.read_excel(destination)
        except Exception as e:
            destination.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=f"Error reading the file: {str(e)}")    
## validate dataset

        if df.empty:
            destination.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")    

## identify columns

        column_names = df.columns.astype(str).tolist()
        numeric_columns = df.select_dtypes(include="number").columns.astype(str).tolist()

        categorical_columns = (
            df.select_dtypes(include=["object", "category"]).columns.astype(str).tolist()
        )        
## generate profile and preview
        
        profile = ProfilingService.generate_profile(df)

        preview_df = df.head(10).copy()

        preview_df = preview_df.astype(object).where(
            pd.notnull(preview_df),
            None,
        )

        preview = preview_df.to_dict(
            orient="records"
        )

## save metadat to database

        dataset = Dataset(
            original_filename=file.filename,
            stored_filename=stored_filename,
            rows=len(df),
            columns=len(df.columns),
            file_size=file_size,
        )   

        try:
            db.add(dataset)
            db.commit()
            db.refresh(dataset)

        except Exception:
            db.rollback()

            destination.unlink(missing_ok=True)

            raise HTTPException(
                status_code=500,
                detail="Failed to save dataset"
            )    




        return {
            "dataset_uuid": dataset.dataset_uuid,
            "original_filename": dataset.original_filename,
            "rows": dataset.rows,
            "columns": dataset.columns,
            "file_size": dataset.file_size,
            "uploaded_at": dataset.uploaded_at,
            "column_names": column_names,
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "preview": preview,
            "profile": profile,
}

    @staticmethod
    def delete_file(file_path: Path):
        """
        Delete a file from the filesystem.
        Raises an HTTPException if the file does not exist.
        """
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found.")
        try:
            file_path.unlink()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
