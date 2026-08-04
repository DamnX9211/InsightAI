interface Props {
  score: number;
}

export default function HealthScoreCard({
  score,
}: Props) {

  const color =
    score >= 85
      ? "text-green-600"
      : score >= 60
      ? "text-yellow-600"
      : "text-red-600";

  const label =
    score >= 85
      ? "Excellent"
      : score >= 60
      ? "Needs Attention"
      : "Poor";

  return (
    <div className="rounded-xl border bg-white p-6 h-full">

      <p className="text-sm text-slate-500">
        Dataset Health
      </p>

      <div className={`mt-5 text-6xl font-bold ${color}`}>
        {score}
      </div>

      <p className="mt-2 text-lg font-medium">
        {label}
      </p>

      <div className="mt-6 h-2 rounded bg-slate-200">

        <div
          className="h-2 rounded bg-green-500"
          style={{
            width: `${score}%`,
          }}
        />

      </div>

    </div>
  );
}