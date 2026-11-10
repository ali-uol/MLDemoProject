from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from src.config import FEATURES
from src.feature_engineering import selection_step

def separate(frame):
    return frame[FEATURES].copy(), frame['species'].copy()

def make_pipeline(select_features=False) -> Pipeline:
    """Imputation and optional selection are fitted within each training fold."""
    return Pipeline([('imputer', SimpleImputer(strategy='median')),
                     ('selection', selection_step(select_features)),
                     ('classifier', DecisionTreeClassifier(random_state=42))])
