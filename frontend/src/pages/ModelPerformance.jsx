import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { modelMetrics, featureImportance, errorMessage } from "../services/api";
export default function ModelPerformance({ info }) {
  const [data, setData] = useState(null),
    [importance, setImportance] = useState([]),
    [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    Promise.all([modelMetrics(), featureImportance()])
      .then(([metrics, features]) => {
        if (active) {
          setData(metrics);
          setImportance(
            Object.entries(features).map(([name, value]) => ({
              name: name.replaceAll("_", " "),
              value,
            })),
          );
        }
      })
      .catch((e) => {
        if (active) setError(errorMessage(e));
      });
    return () => {
      active = false;
    };
  }, []);
  return (
    <>
      <div className="page-heading">
        <span className="eyebrow">MEASURED, NOT ASSUMED</span>
        <h1>Model performance.</h1>
        <p>
          Real results from an untouched 20% test split. Model selection uses
          five-fold cross-validation on training data.
        </p>
      </div>
      {error ? (
        <div className="error-banner" role="alert">
          {error}
        </div>
      ) : !data ? (
        <p role="status">Loading saved metrics?</p>
      ) : (
        <>
          <div className="metric-grid">
            {[
              ["accuracy", "Accuracy"],
              ["precision_macro", "Precision ? macro"],
              ["recall_macro", "Recall ? macro"],
              ["f1_macro", "F1 score ? macro"],
            ].map(([key, title]) => (
              <div className="card metric" key={key}>
                <p>{title}</p>
                <strong>
                  {(data[key] * 100).toFixed(2)}
                  <small>%</small>
                </strong>
                <span>Across {data.test_samples} test flowers</span>
              </div>
            ))}
          </div>
          <div className="workspace-grid">
            <section className="card">
              <h2>Confusion matrix</h2>
              <p>Rows: actual species. Columns: predicted species.</p>
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th scope="col">Actual / predicted</th>
                      {data.class_labels.map((label) => (
                        <th scope="col" key={label}>
                          {label.replace("Iris ", "")}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.confusion_matrix.map((row, i) => (
                      <tr key={i}>
                        <th scope="row">
                          {data.class_labels[i].replace("Iris ", "")}
                        </th>
                        {row.map((value, j) => (
                          <td key={j} className={i === j ? "diagonal" : ""}>
                            {value}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
            <section className="card">
              <h2>Feature importance</h2>
              <p>Relative contribution to impurity reduction.</p>
              <div className="chart">
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart
                    data={importance}
                    layout="vertical"
                    margin={{ left: 20, right: 24 }}
                  >
                    <XAxis type="number" domain={[0, 1]} />
                    <YAxis type="category" dataKey="name" width={100} />
                    <Tooltip />
                    <Bar dataKey="value" fill="#36775e" radius={[0, 5, 5, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <p className="hint">
                The largest bar identifies the measurement with the greatest
                influence on this fitted tree.
              </p>
            </section>
          </div>
          <section className="card detail-card">
            <h2>Training details</h2>
            {info ? (
              <>
                <p>{info.selection.strategy}</p>
                <div className="detail-grid">
                  <span>
                    Training CV baseline{" "}
                    <strong>
                      {(info.selection.baseline_cv_accuracy * 100).toFixed(2)}%
                    </strong>
                  </span>
                  <span>
                    Training CV tuned{" "}
                    <strong>
                      {(info.selection.tuned_cv_accuracy * 100).toFixed(2)}%
                    </strong>
                  </span>
                  <span>
                    Selected model <strong>{info.selection.selected}</strong>
                  </span>
                  <span>
                    Trained{" "}
                    <strong>
                      {new Date(info.training_date).toLocaleString()}
                    </strong>
                  </span>
                </div>
                <pre>{JSON.stringify(info.hyperparameters, null, 2)}</pre>
              </>
            ) : (
              <p>Model metadata is unavailable.</p>
            )}
            <h3>Weighted metrics</h3>
            <p>
              Precision {(data.precision_weighted * 100).toFixed(2)}% ? Recall{" "}
              {(data.recall_weighted * 100).toFixed(2)}% ? F1{" "}
              {(data.f1_weighted * 100).toFixed(2)}%
            </p>
          </section>
        </>
      )}
    </>
  );
}
