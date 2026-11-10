import json
import logging
import joblib
import pandas as pd
from src.config import FEATURES, LABELS
from src.feature_engineering import importance

class PredictionService:
    def __init__(self, root):
        self.root = root
        self.model = None
        self.metadata = None
        self.metrics = None

    def load(self) -> None:
        """Load trusted local training artifacts once; never retrain on startup."""
        try:
            model = joblib.load(self.root/'models/iris_decision_tree.joblib')
            metadata = json.loads((self.root/'models/model_metadata.json').read_text())
            metrics = metadata.get('metrics')
            if (metadata['feature_names'] != FEATURES
                    or list(model.feature_names_in_) != FEATURES
                    or list(model.classes_) != [0, 1, 2]
                    or metadata['class_labels'] != LABELS):
                raise ValueError('Incompatible model schema')
            self.model, self.metadata, self.metrics = model, metadata, metrics
            logging.info('event=model_loaded version=%s', metadata['model_version'])
        except Exception:
            self.model = self.metadata = self.metrics = None
            logging.exception('Model unavailable: check the trusted model and metadata in models/')

    def predict(self, measurements) -> dict:
        frame = pd.DataFrame([measurements],columns=self.metadata['feature_names'])
        predicted = int(self.model.predict(frame)[0])
        probabilities = self.model.predict_proba(frame)[0]
        mapped = {self.metadata['class_labels'][int(label)]:float(prob) for label,prob in zip(self.model.classes_,probabilities)}
        return {'predicted_class':predicted,'predicted_species':self.metadata['class_labels'][predicted],
                'confidence':mapped[self.metadata['class_labels'][predicted]],'class_probabilities':mapped,
                'model_version':self.metadata['model_version']}

    def feature_importance(self) -> dict:
        return importance(self.model)
