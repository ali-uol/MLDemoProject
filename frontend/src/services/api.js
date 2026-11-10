import axios from "axios";
const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  timeout: 15000,
});
export const health = () => client.get("/api/health").then((r) => r.data);
export const predict = (values) =>
  client.post("/api/predict", values).then((r) => r.data);
export const modelInfo = () =>
  client.get("/api/model/info").then((r) => r.data);
export const modelMetrics = () =>
  client.get("/api/model/metrics").then((r) => r.data);
export const featureImportance = () =>
  client.get("/api/model/feature-importance").then((r) => r.data);
export function errorMessage(error) {
  if (!error.response)
    return "Cannot reach the backend. Start FastAPI on port 8000 and try again.";
  const detail = error.response.data?.detail;
  return typeof detail === "string"
    ? detail
    : "The request could not be completed. Check your measurements and try again.";
}
