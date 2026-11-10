import logging
import pandas as pd
from sklearn.datasets import load_iris
from src.config import ROOT, FEATURES

def ingest(root=ROOT) -> pd.DataFrame:
    """Load the canonical built-in dataset; no download or identifier feature."""
    try:
        iris = load_iris()
        frame = pd.DataFrame(iris.data, columns=FEATURES)
        frame['species'] = iris.target
        path = root / 'data/raw/iris.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(path, index=False)
        logging.info('Dataset shape=%s columns=%s first rows=%s classes=%s', frame.shape,
                     list(frame.columns), frame.head().to_dict('records'), frame.species.value_counts().to_dict())
        return frame
    except Exception:
        logging.exception('Data ingestion failed')
        raise
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    ingest()
