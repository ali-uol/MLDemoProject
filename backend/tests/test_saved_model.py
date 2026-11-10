"""Prediction checks using existing artifacts, without training."""
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import create_app

BACKEND = Path(__file__).resolve().parents[1]
SAMPLE = dict(sepal_length=5.1, sepal_width=3.5, petal_length=1.4, petal_width=0.2)

def test_prediction_without_reports(tmp_path):
    shutil.copytree(BACKEND / 'models', tmp_path / 'models')
    with TestClient(create_app(tmp_path)) as client:
        assert client.get('/api/health').status_code == 200
        assert client.get('/docs').status_code == 200
        assert '/api/predict' in client.get('/openapi.json').json()['paths']
        result = client.post('/api/predict', json=SAMPLE)
        assert result.status_code == 200
        assert result.json()['predicted_species'] == 'Iris Setosa'
        for value in ['5.1', 0, -1, True, None]:
            assert client.post('/api/predict', json={**SAMPLE, 'sepal_length': value}).status_code == 422
        assert client.post('/api/predict', json={}).status_code == 422
        assert client.post('/api/predict', json={**SAMPLE, 'extra': 1}).status_code == 422
        for endpoint in ['info', 'metrics', 'feature-importance']:
            assert client.get('/api/model/' + endpoint).status_code == 200

def test_missing_model(tmp_path):
    with TestClient(create_app(tmp_path)) as client:
        assert client.post('/api/predict', json=SAMPLE).status_code == 503

def test_incompatible_metadata(tmp_path):
    import json
    shutil.copytree(BACKEND / 'models', tmp_path / 'models')
    path = tmp_path / 'models/model_metadata.json'
    metadata = json.loads(path.read_text())
    metadata['feature_names'] = list(reversed(metadata['feature_names']))
    path.write_text(json.dumps(metadata))
    with TestClient(create_app(tmp_path)) as client:
        assert client.get('/api/health').status_code == 503
        assert client.post('/api/predict', json=SAMPLE).status_code == 503
