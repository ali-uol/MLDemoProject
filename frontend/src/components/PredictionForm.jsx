import { useState } from "react";

export const examples = {
  sepal_length: "5.1",
  sepal_width: "3.5",
  petal_length: "1.4",
  petal_width: "0.2",
};

export const labels = {
  sepal_length: "Sepal length",
  sepal_width: "Sepal width",
  petal_length: "Petal length",
  petal_width: "Petal width",
};

export default function PredictionForm({ onPredict, loading }) {
  const [values, setValues] = useState(examples);
  const [errors, setErrors] = useState({});

  function submit(event) {
    event.preventDefault();
    const nextErrors = {};
    const measurements = {};
    for (const [name, value] of Object.entries(values)) {
      measurements[name] = Number(value);
      if (!value.trim() || !Number.isFinite(measurements[name]) || measurements[name] <= 0) {
        nextErrors[name] = "Enter a positive measurement in cm.";
      }
    }
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length === 0) onPredict(measurements);
  }

  return (
    <section>
      <form onSubmit={submit} noValidate>
        {Object.entries(labels).map(([name, label]) => (
          <div className="field" key={name}>
            <label htmlFor={name}>{label} (cm)</label>
            <input
              id={name}
              type="number"
              min="0"
              step="any"
              value={values[name]}
              disabled={loading}
              onChange={(event) => setValues({ ...values, [name]: event.target.value })}
              aria-invalid={!!errors[name]}
              aria-describedby={errors[name] ? `${name}-error` : undefined}
            />
            {errors[name] && <p className="error" id={`${name}-error`}>{errors[name]}</p>}
          </div>
        ))}
        <div className="buttons">
          <button type="submit" disabled={loading}>{loading ? "Predicting..." : "Predict"}</button>
        </div>
      </form>
    </section>
  );
}
