export interface DatasetProfile {
    missing_values: Record<string, number>;
    missing_percentage: Record<string, number>;
    duplicate_rows: number;
    column_types: Record<string, number>;

    numeric_statistics: Record<string, Record<string, number | string | null >>;
    categorical_statistics: Record<string, Record<string, number | string | null>>;
}

export interface DatasetResponse {
    dataset_uuid: string;
    original_filename: string;
    rows: number;
    columns: number;
    file_size: number;
    uploaded_at: string;
    column_names: string[];
    numeric_columns: string[];
    categorical_columns: string[];
    preview: Record<string, unknown>[];
    profile: DatasetProfile;
}