import type { DatasetResponse } from "../../types/dataset";

interface DataPreviewProps {
  dataset: DatasetResponse;
}

export default function DataPreview({
  dataset,
}: DataPreviewProps) {
  if (dataset.preview.length === 0) {
    return null;
  }

  return (
    <section className="mt-10">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-slate-950">
          Data preview
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          First {dataset.preview.length} rows from the uploaded dataset.
        </p>
      </div>

      <div className="overflow-x-auto border border-slate-200 bg-white">
        <table className="min-w-full border-collapse text-left text-sm">
          <thead className="bg-slate-50">
            <tr>
              {dataset.column_names.map((column) => (
                <th
                  key={column}
                  className="whitespace-nowrap border-b border-slate-200 px-4 py-3 font-medium text-slate-600"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {dataset.preview.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="border-b border-slate-100 last:border-b-0"
              >
                {dataset.column_names.map((column) => (
                  <td
                    key={column}
                    className="max-w-xs whitespace-nowrap px-4 py-3 text-slate-700"
                  >
                    {row[column] === null ||
                    row[column] === undefined
                      ? "—"
                      : String(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}