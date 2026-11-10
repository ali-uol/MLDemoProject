from typing import Annotated, Any
from pydantic import BaseModel, ConfigDict, Field
Measurement = Annotated[float, Field(strict=True, gt=0, allow_inf_nan=False)]
class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    sepal_length: Measurement
    sepal_width: Measurement
    petal_length: Measurement
    petal_width: Measurement
class PredictionResponse(BaseModel):
    predicted_class: int
    predicted_species: str
    confidence: float
    class_probabilities: dict[str, float]
    model_version: str
class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
class ModelInfo(BaseModel):
    model_name: str
    model_version: str
    algorithm: str
    feature_names: list[str]
    class_labels: list[str]
    training_date: str
    hyperparameters: dict[str, Any]
    metrics: dict[str, Any]
    selection: dict[str, Any]
    feature_importance: dict[str, float]
    sklearn_version: str
class MetricsResponse(BaseModel):
    accuracy: float
    test_samples: int
    precision_macro: float
    precision_weighted: float
    recall_macro: float
    recall_weighted: float
    f1_macro: float
    f1_weighted: float
    confusion_matrix: list[list[int]]
    classification_report: dict[str, Any]
    class_labels: list[str]
