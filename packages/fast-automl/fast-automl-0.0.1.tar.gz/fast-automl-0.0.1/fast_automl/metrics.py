"""# Metrics"""

from sklearn.metrics import (
    r2_score, roc_auc_score as roc_auc_score_base, make_scorer
)

def check_scoring(scoring, classifier):
    """
    Creates a default regression or classifier scoring rule. This is R-squared for regressors and ROC AUC for classifiers.

    Parameters
    ----------
    scoring : str or callable
        A str (see scikit-learn's model evaluation docs) or a scorer callable with signature `scorer(estimator, X, y)` which returns a single value.

    classifier : bool
        Indicates that the estimator is a classifier.
    """
    if scoring is not None:
        return scoring
    return roc_auc_scorer if classifier else make_scorer(r2_score)

def roc_auc_score(y, output):
    """
    Parameters
    ----------
    y : array-like of shape (n_samples,)
        target values.

    output : array-like of shape (n_samples, n_classes)
        Predicted probability of each class.

    Returns
    -------
    score : scalar
        ROC AUC score, default is one-versus-rest for multi-class problems.    
    """
    if len(output.shape) == 1:
        # binary classifier
        return roc_auc_score_base(y, output)
    # multi-class
    return roc_auc_score_base(y, output, multi_class='ovr')

roc_auc_scorer = make_scorer(roc_auc_score, needs_proba=True)