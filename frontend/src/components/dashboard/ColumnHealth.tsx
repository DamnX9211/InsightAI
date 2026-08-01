import type { DatasetResponse } from "../../types/dataset";

interface Props {
  dataset: DatasetResponse;
}

export default function ColumnHealth({
  dataset,
}: Props) {

  return (
    <section className="mt-10">

      <h2 className="text-lg font-semibold mb-4">
        Column Health
      </h2>

      <div className="overflow-hidden rounded border">

        {dataset.column_names.map((column) => {

          const missing =
            dataset.profile.missing_values[column] ?? 0;

          const percent =
            dataset.profile.missing_percentage[column] ?? 0;

          const type =
            dataset.profile.column_types[column];

          return (

            <div
              key={column}
              className="flex justify-between items-center border-b last:border-0 px-5 py-4"
            >

              <div>

                <div className="font-medium">
                  {column}
                </div>

                <div className="text-sm text-slate-500">
                  {type}
                </div>

              </div>

              <div className="text-right">

                <div className="font-medium">
                  {missing}
                </div>

                <div className="text-sm text-slate-500">
                  {percent}%
                </div>

              </div>

            </div>

          );

        })}

      </div>

    </section>
  );

}