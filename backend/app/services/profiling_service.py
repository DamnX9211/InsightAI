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

        numeric_statistics = (
            df.select_dtypes(include="number")
            .describe()
            .round(2)
            .to_dict()
        )

        categorical_statistics = {}

        categorical_df = df.select_dtypes(
            include=["object", "category"]
        )

        for column in categorical_df.columns:
            series = categorical_df[column]

            categorical_statistics[column] = {
               "unique": int(series.nunique()),
               "top": (
                   str(series.mode().iloc[0]) if not series.mode().empty else None
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