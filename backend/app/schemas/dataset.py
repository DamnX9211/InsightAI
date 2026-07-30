from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DatasetProfile(BaseModel):
    missing_values: dict[str, int]  
    missing_percentage: dict[str, float]
    duplicate_rows: int
    column_types: dict[str, str]  


class DatasetResponse(BaseModel):
    dataset_uuid: str
    original_filename: str
    rows: int
    columns: int
    file_size: int
    uploaded_at: datetime

    column_names: list[str]
    numeric_columns: list[str]
    categorical_columns: list[str]
    profile: DatasetProfile



