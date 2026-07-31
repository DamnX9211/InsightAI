import type { DatasetResponse } from "../../types/dataset";

interface DatasetOverviewProps {
  dataset: DatasetResponse;
}

function formatFileSize(bytes: number) {
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function DatasetOverview({
  dataset,
}: DatasetOverviewProps) {
  const totalMissing = Object.values(
    dataset.profile.missing_values
  ).reduce((sum, value) => sum + value, 0);

  const metrics = [
    {
      label: "Rows",
      value: dataset.rows.toLocaleString(),
    },
    {
      label: "Columns",
      value: dataset.columns.toLocaleString(),
    },
    {
      label: "Missing values",
      value: totalMissing.toLocaleString(),
    },
    {
      label: "Duplicate rows",
      value: dataset.profile.duplicate_rows.toLocaleString(),
    },
    {
      label: "File size",
      value: formatFileSize(dataset.file_size),
    },
  ];

  return (
    <section className="mt-10">
      <div className="flex items-end justify-between border-b border-slate-200 pb-5">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-500">
            Dataset
          </p>

          <h2 className="mt-1 text-xl font-semibold text-slate-950">
            {dataset.original_filename}
          </h2>
        </div>

        <p className="text-sm text-slate-500">
          {dataset.numeric_columns.length} numeric ·{" "}
          {dataset.categorical_columns.length} categorical
        </p>
      </div>

      <div className="grid grid-cols-2 border-b border-slate-200 md:grid-cols-5">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="border-r border-slate-200 px-5 py-6 first:pl-0 last:border-r-0"
          >
            <p className="text-sm text-slate-500">
              {metric.label}
            </p>

            <p className="mt-2 text-2xl font-semibold tracking-tight text-slate-950">
              {metric.value}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}