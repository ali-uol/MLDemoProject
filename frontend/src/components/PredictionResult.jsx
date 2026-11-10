export default function PredictionResult({ result }) {
  if (!result) return null;

  return (
    <section className="output" aria-live="polite">
      <h2>Prediction result</h2>
      <p>Predicted species: <strong>{result.predicted_species}</strong></p>
    </section>
  );
}
