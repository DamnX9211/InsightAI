import pandas as pd

class ProfilingService:

    @staticmethod
    def generate_profile(df: pd.DataFrame) -> dict:
        missing_values = df.isnull().sum().to_dict()

        missing_percentage = (
            df.isnull().mean().mul(100).round(2).to_dict()
        )

        duplicate_rows = int(df.duplicated().sum())

        columns_types = {
            column: str(dtype) for column, dtype in df.dtypes.items()
        }

        return {
            "missing_values": missing_values,
            "missing_percentage": missing_percentage,
            "duplicate_rows": duplicate_rows,
            "column_types": columns_types
        }