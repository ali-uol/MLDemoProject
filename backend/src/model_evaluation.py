import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from sklearn.tree import plot_tree
from src.config import FEATURES, LABELS, save_json
from src.feature_engineering import importance

def evaluate(model, x, y, root):
    predicted = model.predict(x)
    metrics = {'accuracy': float(accuracy_score(y,predicted)), 'test_samples': len(y)}
    for average in ['macro','weighted']:
        p,r,f,_ = precision_recall_fscore_support(y,predicted,average=average,zero_division=0)
        metrics.update({f'precision_{average}': float(p),f'recall_{average}':float(r),f'f1_{average}':float(f)})
    metrics['confusion_matrix'] = confusion_matrix(y,predicted,labels=[0,1,2]).tolist()
    metrics['classification_report'] = classification_report(y,predicted,labels=[0,1,2],target_names=LABELS,output_dict=True,zero_division=0)
    metrics['class_labels'] = LABELS
    save_json(root/'reports/metrics.json',metrics)
    figures = root/'reports/figures'
    figures.mkdir(parents=True,exist_ok=True)
    sns.heatmap(metrics['confusion_matrix'],annot=True,fmt='d',xticklabels=LABELS,yticklabels=LABELS,cmap='Greens')
    plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.tight_layout(); plt.savefig(figures/'confusion_matrix.png'); plt.close()
    plt.figure(figsize=(18,10)); plot_tree(model.named_steps['classifier'],feature_names=FEATURES,class_names=LABELS,filled=True,rounded=True)
    plt.savefig(figures/'decision_tree.png',bbox_inches='tight'); plt.close()
    values = importance(model)
    plt.barh(list(values),list(values.values())); plt.xlabel('Impurity-based importance'); plt.tight_layout()
    plt.savefig(figures/'feature_importance.png'); plt.close()
    return metrics
