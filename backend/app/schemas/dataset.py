from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DatasetResponse(BaseModel):
    dataset_uuid: str
    original_filename: str
    rows: int
    columns: int
    file_size: int
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)