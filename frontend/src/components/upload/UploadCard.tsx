import { useRef, useState } from "react";

interface UploadCardProps {
  onFileSelect: (file: File) => void;
  isUploading: boolean;
}

export default function UploadCard({
  onFileSelect,
  isUploading,
}: UploadCardProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFile = (file: File) => {
    const allowedExtensions = [".csv", ".xlsx", ".xls"];

    const extension = file.name
      .substring(file.name.lastIndexOf("."))
      .toLowerCase();

    if (!allowedExtensions.includes(extension)) {
      alert("Please select a CSV or Excel file.");
      return;
    }

    setSelectedFile(file);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();

    setIsDragging(false);

    const file = event.dataTransfer.files[0];

    if (file) {
      handleFile(file);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      onFileSelect(selectedFile);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="w-full max-w-2xl">
      <div
        onDragOver={(event) => {
          event.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed p-10 text-center transition ${
          isDragging
            ? "border-slate-500 bg-slate-50"
            : "border-slate-300 bg-white"
        }`}
      >
        <div className="mx-auto mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-slate-100">
          <span className="text-xl">↑</span>
        </div>

        <h2 className="text-lg font-semibold text-slate-900">
          Upload a dataset
        </h2>

        <p className="mt-2 text-sm text-slate-500">
          Drop a CSV or Excel file here, or choose one from your computer.
        </p>

        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          disabled={isUploading}
          className="mt-6 border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Browse files
        </button>

        <input
          ref={inputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          className="hidden"
          onChange={(event) => {
            const file = event.target.files?.[0];

            if (file) {
              handleFile(file);
            }
          }}
        />

        <p className="mt-4 text-xs text-slate-400">
          CSV, XLSX or XLS · Maximum 100 MB
        </p>
      </div>

      {selectedFile && (
        <div className="mt-4 flex items-center justify-between border border-slate-200 bg-white p-4">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-slate-800">
              {selectedFile.name}
            </p>

            <p className="mt-1 text-xs text-slate-500">
              {formatFileSize(selectedFile.size)}
            </p>
          </div>

          <button
            type="button"
            disabled={isUploading}
            onClick={handleUpload}
            className="ml-4 bg-slate-900 px-5 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isUploading ? "Analyzing..." : "Analyze dataset"}
          </button>
        </div>
      )}
    </div>
  );
}