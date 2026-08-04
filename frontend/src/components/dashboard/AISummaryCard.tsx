import type { DatasetResponse } from "../../types/dataset";

interface Props {
  summary: DatasetResponse["summary"];
}

export default function AISummaryCard({
  summary,
}: Props) {
  return (
    <div className="rounded-xl border bg-white p-6 h-full">

      <h2 className="text-lg font-semibold">
        AI Analysis
      </h2>

      <div className="mt-6 space-y-6">

        <div>
          <p className="text-sm text-slate-500">
            Overall Quality
          </p>

          <p className="mt-1 text-lg font-semibold">
            {summary.overall_quality}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500">
            ML Readiness
          </p>

          <p className="mt-1 text-lg font-semibold">
            {summary.ml_readiness}
          </p>
        </div>

        <div>
          <p className="text-sm text-slate-500 mb-2">
            Critical Issues
          </p>

          <ul className="space-y-2 list-disc pl-5">
            {summary.critical_issues.map((issue, index) => (
              <li key={index}>{issue}</li>
            ))}
          </ul>
        </div>

        <div>
          <p className="text-sm text-slate-500 mb-2">
            Recommendations
          </p>

          <ul className="space-y-2 list-disc pl-5">
            {summary.recommendations.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>

      </div>

    </div>
  );
}