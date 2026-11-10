import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import ROOT, FEATURES, LABELS, save_json

def eda(frame, root=ROOT):
    """Descriptive EDA only; the training workflow passes training observations."""
    destination = root / 'reports/figures'
    destination.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style='whitegrid')
    data = frame.copy()
    data['species'] = data.species.map(dict(enumerate(LABELS)))
    save_json(root / 'reports/eda_summary.json', {'rows': len(data), 'statistics': data[FEATURES].describe().to_dict(), 'missing_values': data.isna().sum().to_dict()})
    def save(name):
        plt.tight_layout()
        plt.savefig(destination / name, dpi=140, bbox_inches='tight')
        plt.close('all')
    sns.countplot(data=data, x='species'); save('class_distribution.png')
    data[FEATURES].hist(figsize=(10,7)); save('feature_histograms.png')
    sns.heatmap(data[FEATURES].corr(), annot=True, cmap='viridis'); save('correlation.png')
    sns.pairplot(data, hue='species', diag_kind='hist'); save('pairplot.png')
    fig, axes = plt.subplots(2,2,figsize=(12,8))
    for name, ax in zip(FEATURES, axes.flat): sns.boxplot(data=data,x='species',y=name,ax=ax)
    save('boxplots.png')
if __name__ == '__main__':
    from src.data_ingestion import ingest
    eda(ingest())
