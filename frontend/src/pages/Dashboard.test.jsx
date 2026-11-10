import { it, expect, vi } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Dashboard from "./Dashboard";
import { predict } from "../services/api";
vi.mock("../services/api", () => ({
  predict: vi.fn(),
  errorMessage: () => "Cannot reach the backend.",
}));
it("displays the predicted species from the API", async () => {
  predict.mockResolvedValueOnce({
    predicted_species: "Iris Setosa",
    confidence: 1,
    class_probabilities: {
      "Iris Setosa": 1,
      "Iris Versicolor": 0,
      "Iris Virginica": 0,
    },
    model_version: "1.0.0",
  });
  render(<Dashboard />);
  fireEvent.click(screen.getByRole("button", { name: /^Predict$/ }));
  await waitFor(() =>
    expect(
      screen.getByText("Iris Setosa", { exact: false }),
    ).toBeInTheDocument(),
  );
  expect(screen.getByText("Iris Setosa")).toBeInTheDocument();

});
it("shows a network error", async () => {
  predict.mockRejectedValueOnce(new Error("offline"));
  render(<Dashboard />);
  fireEvent.click(screen.getByRole("button", { name: /^Predict$/ }));
  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Cannot reach the backend.",
  );
});
