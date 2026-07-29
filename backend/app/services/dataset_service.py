from pathlib import Path
import shutil

from fastapi import UploadFile, HTTPException

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

class DatasetService:
    @staticmethod
    async def save_file(file: UploadFile) -> Path:
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
        return destination

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
