from pathlib import Path
import os
import json
from dotenv import load_dotenv
BASE = Path(__file__).resolve().parents[1]
load_dotenv(BASE / '.env')
ROOT = Path(os.getenv('IRIS_ARTIFACT_DIR') or BASE)
ROOT = (ROOT if ROOT.is_absolute() else BASE / ROOT).resolve()
FEATURES = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
LABELS = ['Iris Setosa', 'Iris Versicolor', 'Iris Virginica']
def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')
