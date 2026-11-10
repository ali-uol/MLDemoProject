import numpy as np
import pandas as pd
from src.config import ROOT, FEATURES, save_json

def validate(frame: pd.DataFrame, root=ROOT) -> dict:
    """Report critical errors and preserve legitimate duplicate measurements."""
    errors, warnings = [], []
    if frame.empty: errors.append('Dataset is empty')
    if set(frame.columns) != set(FEATURES + ['species']): errors.append('Unexpected or missing columns')
    if not errors:
        for name in FEATURES:
            if not pd.api.types.is_numeric_dtype(frame[name]) or pd.api.types.is_bool_dtype(frame[name]):
                errors.append(f'{name}: expected numeric dtype')
                continue
            present = frame[name].dropna()
            if not np.isfinite(present).all(): errors.append(f'{name}: non-finite values')
            if (present <= 0).any(): errors.append(f'{name}: measurements must be positive')
            if frame[name].isna().any(): warnings.append(f'{name}: missing values will be imputed on training folds')
            if frame[name].isna().all(): errors.append(f'{name}: no observed measurements')
        if not pd.api.types.is_integer_dtype(frame.species) or not frame.species.isin([0,1,2]).all():
            errors.append('Target must contain integer labels 0, 1, 2 without missing values')
        counts = frame.species.value_counts()
        if set(counts.index) != {0,1,2} or counts.min() < 7: errors.append('Each species needs at least seven observations for stratified CV')
        if counts.nunique() > 1: warnings.append('Class distribution is imbalanced')
    duplicates = int(frame.duplicated().sum())
    if duplicates: warnings.append(f'{duplicates} duplicate observations retained')
    report = {'valid': not errors, 'errors': errors, 'warnings': warnings,
              'rows': len(frame), 'duplicates': duplicates,
              'missing_values': frame.isna().sum().to_dict(),
              'class_distribution': {str(key): int(value) for key, value in frame.species.value_counts().items()} if 'species' in frame else {}}
    save_json(root / 'reports/validation.json', report)
    if errors: raise ValueError('Data validation failed: ' + '; '.join(errors))
    return report
