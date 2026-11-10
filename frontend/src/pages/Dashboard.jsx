import { useState } from "react";
import PredictionForm from "../components/PredictionForm";
import PredictionResult from "../components/PredictionResult";
import { predict, errorMessage } from "../services/api";

export default function Dashboard() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function classify(values) {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      setResult(await predict(values));
    } catch (error) {
      setError(errorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Iris Flower Classification</h1>
      <p className="description">
        This student project uses a Decision Tree model to predict the Iris
        flower species. Enter the sepal and petal measurements in centimeters
        to classify a flower as Setosa, Versicolor, or Virginica.
      </p>
      <PredictionForm onPredict={classify} loading={loading} />
      {error && <p className="error" role="alert">{error}</p>}
      <PredictionResult result={result} />
    </main>
  );
}
