import pandas as pd
from typing import Any

class ProfilingService:

    @staticmethod
    def generate_profile(df: pd.DataFrame) -> dict[str, Any]:

        missing_values = {
            column: int(value)
            for column, value in df.isnull().sum().items()
        }

        missing_percentage = {
            column: float(value)
            for column, value in ( df.isnull().mean().mul(100).round(2).items())
        }

        duplicate_rows = int(df.duplicated().sum())

        columns_types = {
            column: str(dtype) for column, dtype in df.dtypes.items()
        }

        numeric_df = df.select_dtypes(include="number")

        if not numeric_df.empty and len(numeric_df.columns) > 0:
            numeric_statistics = (
                numeric_df.describe().round(2).to_dict()
            )
        else:
            numeric_statistics = {}

        categorical_statistics = {}

        categorical_df = df.select_dtypes(
            include=["object", "category"]
        )

        for column in categorical_df.columns:
            series = categorical_df[column]

            mode = series.mode()

            categorical_statistics[column] = {
               "unique": int(series.nunique()),
               "top": (
                   str(mode.iloc[0]) if not mode.empty else None
               ),
               "missing": int(series.isnull().sum()),
               "missing_percentage": round(series.isnull().mean() * 100, 2),
            }

        return {
            "missing_values": missing_values,
            "missing_percentage": missing_percentage,
            "duplicate_rows": duplicate_rows,
            "column_types": columns_types,
            "numeric_statistics": numeric_statistics,
            "categorical_statistics": categorical_statistics,
        }