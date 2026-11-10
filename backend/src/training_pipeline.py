import logging
from datetime import datetime, timezone
import joblib
import sklearn
from sklearn.model_selection import train_test_split
from src.config import ROOT, FEATURES, LABELS, save_json
from src.data_ingestion import ingest
from src.data_validation import validate
from src.data_preprocessing import separate
from src.eda import eda
from src.model_training import train
from src.model_evaluation import evaluate
from src.feature_engineering import importance

def run(root=ROOT, with_eda=True):
    for directory in ['logs','models','data/processed']: (root/directory).mkdir(parents=True,exist_ok=True)
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.StreamHandler(),logging.FileHandler(root/'logs/training.log')])
    frame = ingest(root); validate(frame,root)
    x,y = separate(frame)
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,stratify=y,random_state=42)
    # Split before EDA so test observations cannot influence exploration or tuning.
    for name, xx, yy in [('train',x_train,y_train),('test',x_test,y_test)]:
        xx.assign(species=yy).to_csv(root/f'data/processed/{name}.csv',index=False)
    if with_eda: eda(x_train.assign(species=y_train),root)
    logging.info('Training baseline and searching 90 parameter combinations on five folds')
    model, selection = train(x_train,y_train)
    metrics = evaluate(model,x_test,y_test,root)
    metadata = {'model_name':'Iris Decision Tree','model_version':'1.0.0','algorithm':'DecisionTreeClassifier',
                'feature_names':FEATURES,'class_labels':LABELS,'training_date':datetime.now(timezone.utc).isoformat(),
                'hyperparameters':model.named_steps['classifier'].get_params(),'metrics':metrics,
                'selection':selection,'feature_importance':importance(model),'sklearn_version':sklearn.__version__}
    joblib.dump(model,root/'models/iris_decision_tree.joblib')
    save_json(root/'models/model_metadata.json',metadata)
    logging.info('Model saved. Test accuracy: %.4f; selection=%s',metrics['accuracy'],selection)
    return model, metadata
if __name__ == '__main__':
    run()
