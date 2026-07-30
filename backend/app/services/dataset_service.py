from pathlib import Path
import shutil
import pandas as pd
from sqlalchemy.orm import Session

from app.models.dataset import Dataset

from fastapi import UploadFile, HTTPException

from app.services.profiling_service import ProfilingService

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

class DatasetService:
    @staticmethod
    async def upload_dataset(file: UploadFile, db: Session):
        """
        Save the uploaded file to the UPLOAD_DIR.
        Raises an HTTPException if the file extension is not allowed.
        """
        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid file type. Only CSV and Excel files are allowed.")

        destination = UPLOAD_DIR / file.filename
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if extension == ".csv":
            df = pd.read_csv(destination)
        else: 
            df = pd.read_excel(destination)   

        profile = ProfilingService.generate_profile(df)    

        numeric_columns = df.select_dtypes(include="number").columns.tolist()

        categorical_columns = (
            df.select_dtypes(include=["object", "category"]).columns.tolist()
        )        

        column_names = df.columns.tolist()

        dataset = Dataset(
            original_filename=file.filename,
            stored_filename=destination.name,
            rows=len(df),
            columns=len(df.columns),
            file_size=destination.stat().st_size
        )   

        db.add(dataset)
        db.commit()
        db.refresh(dataset)


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
