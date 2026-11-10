import json
import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from src.data_ingestion import ingest
from src.data_validation import validate
from src.config import FEATURES

def test_dataset(tmp_path):
    frame=ingest(tmp_path)
    assert frame.shape == (150,5)
    assert list(frame.columns) == FEATURES+['species']
    assert validate(frame,tmp_path)['valid']
@pytest.mark.parametrize('value',[-1,0,float('inf'),'bad'])
def test_invalid_measurement(tmp_path,value):
    frame=ingest(tmp_path)
    if isinstance(value,str): frame['sepal_length']=frame.sepal_length.astype(object)
    frame.loc[0,'sepal_length']=value
    with pytest.raises(ValueError): validate(frame,tmp_path)

def test_validation_schema_target_and_empty(tmp_path):
    frame=ingest(tmp_path)
    for invalid in [frame.iloc[:0],frame.drop(columns=['petal_width']),frame.assign(species=99),frame.assign(extra=1)]:
        with pytest.raises(ValueError): validate(invalid,tmp_path)

def test_missing_and_duplicates_are_warnings(tmp_path):
    frame=ingest(tmp_path)
    frame.loc[0,'sepal_length']=np.nan
    frame=pd.concat([frame,frame.iloc[[1]]],ignore_index=True)
    report=validate(frame,tmp_path)
    assert report['valid'] and report['duplicates'] > 0 and report['warnings']

def test_training_serialization_and_metrics(artifacts):
    model=joblib.load(artifacts/'models/iris_decision_tree.joblib')
    test=pd.read_csv(artifacts/'data/processed/test.csv')
    predicted=model.predict(test[FEATURES])
    assert set(predicted) <= {0,1,2}
    assert np.allclose(model.predict_proba(test[FEATURES]).sum(axis=1),1)
    metrics=json.loads((artifacts/'reports/metrics.json').read_text())
    assert metrics['accuracy'] == accuracy_score(test.species,predicted)
    assert metrics['confusion_matrix'] == confusion_matrix(test.species,predicted).tolist()
    assert metrics['classification_report'] == classification_report(test.species,predicted,labels=[0,1,2],target_names=metrics['class_labels'],output_dict=True,zero_division=0)
    for average in ['macro','weighted']:
        p,r,f,_=precision_recall_fscore_support(test.species,predicted,average=average,zero_division=0)
        for key,value in [('precision',p),('recall',r),('f1',f)]: assert metrics[f'{key}_{average}'] == pytest.approx(value)

@pytest.mark.parametrize('value',[None,float('nan'),float('inf')])
def test_invalid_target_report(tmp_path,value):
    frame=ingest(tmp_path)
    frame['species']=frame.species.astype(float)
    frame.loc[0,'species']=value
    with pytest.raises(ValueError,match='Data validation failed'): validate(frame,tmp_path)
    assert not json.loads((tmp_path/'reports/validation.json').read_text())['valid']
