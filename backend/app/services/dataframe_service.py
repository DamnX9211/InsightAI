from pathlib import Path

import pandas as pd
from fastapi import HTTPException


class DataFrameService:

    @staticmethod
    def load_dataframe(
        path: Path,
    ) -> pd.DataFrame:

        extension = path.suffix.lower()

        try:

            if extension == ".csv":
                df = pd.read_csv(path)

            else:
                df = pd.read_excel(path)

        except Exception:

            raise HTTPException(
                status_code=400,
                detail="Unable to read dataset.",
            )

        if df.empty:

            raise HTTPException(
                status_code=400,
                detail="Dataset is empty.",
            )

        return df