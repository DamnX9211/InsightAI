from typing import Any

import pandas as pd


class ProfilingService:

    @staticmethod
    def get_column_names(df: pd.DataFrame) -> list[str]:
        return df.columns.astype(str).tolist()

    @staticmethod
    def get_numeric_columns(df: pd.DataFrame) -> list[str]:
        return (
            df.select_dtypes(include="number")
            .columns.astype(str)
            .tolist()
        )

    @staticmethod
    def get_categorical_columns(df: pd.DataFrame) -> list[str]:
        return (
            df.select_dtypes(
                include=["object", "category"]
            )
            .columns.astype(str)
            .tolist()
        )

    @staticmethod
    def get_missing_values(df: pd.DataFrame) -> dict[str, int]:
        return {
            column: int(value)
            for column, value in df.isnull().sum().items()
        }

    @staticmethod
    def get_missing_percentage(df: pd.DataFrame) -> dict[str, float]:
        return {
            column: float(value)
            for column, value in (
                df.isnull()
                .mean()
                .mul(100)
                .round(2)
                .items()
            )
        }

    @staticmethod
    def get_duplicate_rows(df: pd.DataFrame) -> int:
        return int(df.duplicated().sum())

    @staticmethod
    def get_column_types(df: pd.DataFrame) -> dict[str, str]:
        return {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        }

    @staticmethod
    def get_numeric_statistics(
        df: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:

        numeric_df = df.select_dtypes(include="number")

        if numeric_df.empty:
            return {}

        return (
            numeric_df
            .describe()
            .round(2)
            .to_dict()
        )

    @staticmethod
    def get_categorical_statistics(
        df: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:

        statistics = {}

        categorical_df = df.select_dtypes(
            include=["object", "category"]
        )

        for column in categorical_df.columns:

            series = categorical_df[column]

            mode = series.mode()

            statistics[column] = {
                "unique": int(series.nunique()),
                "top": (
                    str(mode.iloc[0])
                    if not mode.empty
                    else None
                ),
                "missing": int(series.isnull().sum()),
            }

        return statistics

    @staticmethod
    def get_preview(
        df: pd.DataFrame,
        rows: int = 10,
    ) -> list[dict]:

        preview_df = df.head(rows).copy()

        preview_df = preview_df.astype(object).where(
            pd.notnull(preview_df),
            None,
        )

        return preview_df.to_dict(
            orient="records"
        )

    @staticmethod
    def generate_profile(
        df: pd.DataFrame,
    ) -> dict[str, Any]:

        return {
            "missing_values":
                ProfilingService.get_missing_values(df),

            "missing_percentage":
                ProfilingService.get_missing_percentage(df),

            "duplicate_rows":
                ProfilingService.get_duplicate_rows(df),

            "column_types":
                ProfilingService.get_column_types(df),

            "numeric_statistics":
                ProfilingService.get_numeric_statistics(df),

            "categorical_statistics":
                ProfilingService.get_categorical_statistics(df),
        }