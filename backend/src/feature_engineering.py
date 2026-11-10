from sklearn.feature_selection import SelectKBest, f_classif
from src.config import FEATURES

def selection_step(enabled=False):
    """Optional ANOVA top-three selection; default retains all four measurements."""
    return SelectKBest(f_classif, k=3) if enabled else 'passthrough'

def importance(model) -> dict:
    selector = model.named_steps['selection']
    names = FEATURES if isinstance(selector, str) else [n for n, keep in zip(FEATURES, selector.get_support()) if keep]
    result = dict.fromkeys(FEATURES, 0.0)
    result.update({name: float(value) for name, value in zip(names, model.named_steps['classifier'].feature_importances_)})
    return result
