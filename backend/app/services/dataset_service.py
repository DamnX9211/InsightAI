from fastapi import UploadFile
from sqlalchemy.orm import Session
import pandas as pd

from app.models.dataset import Dataset
from app.services.storage_service import StorageService
from app.services.dataframe_service import DataFrameService
from app.services.profiling_service import ProfilingService


class DatasetService:

    @staticmethod
    async def upload_dataset(
        file: UploadFile,
        db: Session,
    ) -> dict:

        # Save uploaded file
        destination, file_size, stored_filename = (
            StorageService.save_uploaded_file(file)
        )

        # Load dataframe
        df = DataFrameService.load_dataframe(destination)

        # Dataset information
        column_names = ProfilingService.get_column_names(df)

        numeric_columns = ProfilingService.get_numeric_columns(df)

        categorical_columns = ProfilingService.get_categorical_columns(df)


        # Dataset profile
        profile = ProfilingService.generate_profile(df)

        # Preview
        preview = ProfilingService.get_preview(df)

        # Save metadata to database
        dataset = Dataset(
            original_filename=file.filename,
            stored_filename=stored_filename,
            rows=len(df),
            columns=len(df.columns),
            file_size=file_size,
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
            "preview": preview,
            "profile": profile,
        }