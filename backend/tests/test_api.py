import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.schemas.prediction import PredictionRequest
VALID={'sepal_length':5.1,'sepal_width':3.5,'petal_length':1.4,'petal_width':0.2}
@pytest.fixture
def client(artifacts):
    with TestClient(create_app(artifacts)) as value: yield value

def test_endpoints(client):
    assert client.get('/api/health').json() == {'status':'healthy','model_loaded':True}
    result=client.post('/api/predict',json=VALID)
    assert result.status_code == 200
    assert result.json()['predicted_species'] == 'Iris Setosa'
    assert sum(result.json()['class_probabilities'].values()) == pytest.approx(1)
    for path in ['info','metrics','feature-importance']:
        assert client.get('/api/model/'+path).status_code == 200
    assert sum(client.get('/api/model/feature-importance').json().values()) == pytest.approx(1)
    assert client.get('/docs').status_code == 200
@pytest.mark.parametrize('value',['5.1',0,-1,True,None])
def test_invalid_input(client,value):
    assert client.post('/api/predict',json={**VALID,'sepal_length':value}).status_code == 422
@pytest.mark.parametrize('value',[float('nan'),float('inf'),float('-inf')])
def test_nonfinite(value,client):
    with pytest.raises(ValueError): PredictionRequest(**{**VALID,'sepal_length':value})
    raw='{"sepal_length":'+str(value).replace('nan','NaN').replace('inf','Infinity')+',"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
    assert client.post('/api/predict',content=raw,headers={'Content-Type':'application/json'}).status_code == 422

def test_missing_extra_and_cors(client):
    assert client.post('/api/predict',json={}).status_code == 422
    assert client.post('/api/predict',json={**VALID,'extra':1}).status_code == 422
    result=client.options('/api/predict',headers={'Origin':'http://localhost:5173','Access-Control-Request-Method':'POST'})
    assert result.headers['access-control-allow-origin'] == 'http://localhost:5173'

def test_missing_model(tmp_path):
    with TestClient(create_app(tmp_path)) as client:
        assert client.get('/api/health').status_code == 503
        assert client.post('/api/predict',json=VALID).status_code == 503
        for route in ['info','metrics','feature-importance']: assert client.get('/api/model/'+route).status_code == 503
