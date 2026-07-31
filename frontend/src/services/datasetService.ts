import apiClient from "../api/client";
import type { DatasetResponse } from "../types/dataset";

export async function uploadDataset(
    file: File
): Promise<DatasetResponse> {
    const formData = new FormData();

    formData.append("file", file);

    const response = await apiClient.post<DatasetResponse>(
        "/datasets/upload",
        formData
    );

    return response.data;
}