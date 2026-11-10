import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import PredictionForm from "./PredictionForm";
describe("Prediction form", () => {
  it("submits numeric measurements", () => {
    const submit = vi.fn();
    render(<PredictionForm onPredict={submit} onReset={() => {}} />);
    fireEvent.click(
      screen.getByRole("button", { name: /^Predict$/ }),
    );
    expect(submit).toHaveBeenCalledWith({
      sepal_length: 5.1,
      sepal_width: 3.5,
      petal_length: 1.4,
      petal_width: 0.2,
    });
  });
  it("rejects zero and empty fields", () => {
    const submit = vi.fn();
    render(<PredictionForm onPredict={submit} onReset={() => {}} />);
    fireEvent.change(screen.getByLabelText("Sepal length (cm)"), {
      target: { value: "0" },
    });
    fireEvent.change(screen.getByLabelText("Petal width (cm)"), {
      target: { value: "" },
    });
    fireEvent.click(
      screen.getByRole("button", { name: /^Predict$/ }),
    );
    expect(submit).not.toHaveBeenCalled();
    expect(screen.getAllByText(/Enter a positive/)).toHaveLength(2);
  });
  it("disables controls while loading", () => {
    render(<PredictionForm loading onPredict={() => {}} onReset={() => {}} />);
    expect(screen.getByRole("button", { name: /Predicting/ })).toBeDisabled();
  });
});
