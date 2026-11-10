from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from src.data_preprocessing import make_pipeline

def train(x, y):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    baseline = make_pipeline()
    baseline_score = float(cross_val_score(baseline, x, y, cv=cv, scoring='accuracy').mean())
    grid = {'classifier__criterion': ['gini','entropy'], 'classifier__max_depth': [2,3,4,5,None],
            'classifier__min_samples_split': [2,4,6], 'classifier__min_samples_leaf': [1,2,3]}
    search = GridSearchCV(make_pipeline(), grid, scoring='accuracy', cv=cv, n_jobs=1).fit(x,y)
    # Prefer baseline on a CV tie; no test-set information enters selection.
    use_tuned = search.best_score_ > baseline_score + 1e-12
    model = search.best_estimator_ if use_tuned else baseline.fit(x,y)
    return model, {'baseline_cv_accuracy': baseline_score, 'tuned_cv_accuracy': float(search.best_score_),
                   'selected': 'tuned' if use_tuned else 'baseline',
                   'strategy': 'Higher mean five-fold training CV accuracy; baseline wins ties',
                   'best_grid_parameters': search.best_params_}
