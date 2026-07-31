import { useState } from "react";
import axios from "axios";

import UploadCard from "../components/upload/UploadCard";
import { uploadDataset } from "../services/datasetService";
import type { DatasetResponse } from "../types/dataset";


export default function Upload() {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");
  const [dataset, setDataset] = useState<DatasetResponse | null>(null);

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    setError("");

    try {
      const result = await uploadDataset(file);

      setDataset(result);

      console.log("Dataset analysis:", result);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setError(
          error.response?.data?.detail ??
            "Unable to upload the dataset."
        );
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-6xl px-6 py-10">
        <header className="mb-14">
          <p className="text-sm font-medium text-slate-500">
            InsightAI
          </p>

          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">
            Understand your data before you analyze it.
          </h1>

          <p className="mt-3 max-w-xl text-sm leading-6 text-slate-600">
            Upload a dataset to inspect its structure, data quality,
            distributions, and potential issues.
          </p>
        </header>

        <UploadCard
          onFileSelect={handleUpload}
          isUploading={isUploading}
        />

        {error && (
          <div className="mt-5 max-w-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {dataset && (
          <div className="mt-6 max-w-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
            Analysis complete for{" "}
            <span className="font-medium">
              {dataset.original_filename}
            </span>
          </div>
        )}
      </div>
    </main>
  );
}