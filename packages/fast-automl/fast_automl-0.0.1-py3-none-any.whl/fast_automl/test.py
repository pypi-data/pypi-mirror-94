"""# Model comparison tests"""

from .metrics import check_scoring

import numpy as np
import pandas as pd
from scipy.stats import t as t_distribution
from sklearn.base import clone, is_classifier
from sklearn.model_selection import check_cv
from joblib import Parallel, delayed

def _compute_pairwise_diff(
        estimators, X, y, repetitions, cv, scoring=None, n_jobs=None
    ):
    """
    Returns
    -------
    pairwise_diff : np.array of shape (n_pairs, r*k)
        Array of pairwise differences between estimator scores across 
        repetitions and folds.
    """
    def fold_score(estimator, train_idx, test_idx):
        if isinstance(X, pd.DataFrame):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        else:
            X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        estimator.fit(X_train, y_train)
        return scoring(estimator, X_test, y_test)
    
    scoring = check_scoring(scoring, classifier=is_classifier(estimators[0]))
    cv = check_cv(cv, y=y, classifier=is_classifier(estimators[0]))
    if hasattr(cv, 'shuffle'):
        cv.shuffle = True
    scores = Parallel(n_jobs=n_jobs)(
        delayed(fold_score)(
            clone(est), train_idx, test_idx
        )
        for _ in range(repetitions)
        for train_idx, test_idx in cv.split(X)
        for name, est in estimators
    )
    scores = np.array(scores).reshape(-1, len(estimators))
    return np.array([
        scores[:,i]-scores[:,j]
        for i in range(len(estimators)) 
        for j in range(i+1, len(estimators))
    ]).T

def _collect_dataframe(
        estimators, pairwise_diff_mean, pairwise_diff_std, t_stats, p_vals
    ):
    # collects test results into a pandas dataframe
    df = pd.DataFrame([
        {
            'Estimator1': estimators[i][0],
            'Estimator2': estimators[j][0]
        }
        for i in range(len(estimators))
        for j in range(i+1, len(estimators))
    ])
    df['PerformanceDifference'] = pairwise_diff_mean
    df['Std'] = pairwise_diff_std
    df['t-stat'] = t_stats
    df['p-value'] = p_vals
    return df

def corrected_repeated_kfold_cv_test(
        estimators, X, y, repetitions=10, cv=10, scoring=None, n_jobs=None
    ):
    """
    Performs pairwise corrected repeated k-fold cross-validation tests. See [Bouckaert and Frank](https://www.cs.waikato.ac.nz/~eibe/pubs/bouckaert_and_frank.pdf).

    Parameters
    ----------
    estimators : list
        List of (name, estimator) tuples.

    X : array-like of shape (n_samples, n_features)
        Features.

    y : array-like of shape (n_samples, n_targets)
        Targets.

    repetitions : int, default=10
        Number of cross-validation repetitions.

    cv : int, cross-validation generator, or iterable, default=10
        Scikit-learn style cv parameter.

    scoring : str, callable, list, tuple, or dict, default=None
        Scikit-learn style scoring parameter.

    n_jobs : int, default=None
        Number of jobs to run in parallel.

    Returns
    -------
    results_df : pd.DataFrame

    Examples
    --------
    ```python
    from fast_automl.test import corrected_repeated_kfold_cv_test

    from sklearn.datasets import load_boston
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.svm import SVR

    X, y = load_boston(return_X_y=True)
    corrected_repeated_kfold_cv_test(
    \    [
    \        ('rf', RandomForestRegressor()),
    \        ('ridge', Ridge()),
    \        ('svm', SVR())
    \    ],
    \    X, y, n_jobs=-1
    )
    ```

    Out:

    ```
    Estimator1 Estimator2  PerformanceDifference       Std     t-stat       p-value
    \        rf      ridge               0.165030  0.030266   5.452600  3.652601e-07   
    \        rf        svm               0.670975  0.045753  14.665154  1.460994e-26  
    \     ridge        svm               0.505945  0.045031  11.235469  2.258586e-19
    ```
    """
    cv = check_cv(cv, y=y, classifier=is_classifier(estimators[0]))
    pairwise_diff = _compute_pairwise_diff(
        estimators, X, y, repetitions, cv, scoring, n_jobs
    )
    # Nadeau and Bengio correction
    # https://www.cs.waikato.ac.nz/~eibe/pubs/bouckaert_and_frank.pdf
    pairwise_diff_var = pairwise_diff.var(axis=0, ddof=1)
    k = cv.get_n_splits(X)
    pairwise_diff_var *= 1./(k * repetitions) + 1./(k-1)
    # compute statistics
    pairwise_diff_mean = pairwise_diff.mean(axis=0)
    pairwise_diff_std = np.sqrt(pairwise_diff_var)
    t_stats = pairwise_diff_mean / pairwise_diff_std
    df = k * repetitions - 1
    p_vals = [t_distribution.sf(abs(t_stat), df)*2 for t_stat in t_stats]
    return _collect_dataframe(estimators, pairwise_diff_mean, pairwise_diff_std, t_stats, p_vals)

def r_by_k_cv_test(
        estimators, X, y, repetitions=5, cv=2, scoring=None, n_jobs=None
    ):
    """
    Performs pariwise RxK (usually 5x2) cross-validation tests. See [here](https://www.kaggle.com/ogrellier/parameter-tuning-5-x-2-fold-cv-statistical-test).

    Parameters
    ----------
    estimators : list
        List of (name, estimator) tuples.

    X : array-like of shape (n_samples, n_features)
        Features.

    y : array-like of shape (n_samples, n_targets)
        Targets.

    repetitions : int, default=10
        Number of cross-validation repetitions.

    cv : int, cross-validation generator, or iterable, default=10
        Scikit-learn style cv parameter.

    scoring : str, callable, list, tuple, or dict, default=None
        Scikit-learn style scoring parameter.

    n_jobs : int, default=None
        Number of jobs to run in parallel.

    Returns
    -------
    results_df : pd.DataFrame

    Examples
    --------
    ```python
    from fast_automl.test import r_by_k_cv_test

    from sklearn.datasets import load_boston
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import Ridge
    from sklearn.svm import SVR

    X, y = load_boston(return_X_y=True)
    r_by_k_cv_test(
    \    [
    \        ('rf', RandomForestRegressor()),
    \        ('ridge', Ridge()),
    \        ('svm', SVR())
    \    ],
    \    X, y, n_jobs=-1
    )
    ```

    Out:

    ```
    Estimator1 Estimator2  PerformanceDifference       Std     t-stat   p-value
    \        rf      ridge               0.143314  0.026026   5.506631  0.002701
    \        rf        svm               0.659547  0.035824  18.410644  0.000009
    \     ridge        svm               0.516233  0.021601  23.898480  0.000002
    ```
    """
    cv = check_cv(cv, y=y, classifier=is_classifier(estimators[0]))
    pairwise_diff = _compute_pairwise_diff(
        estimators, X, y, repetitions, cv, scoring, n_jobs
    )
    # compute variance of performance difference across folds
    n_pairs = int(.5 * len(estimators) * (len(estimators)-1))
    diff = pairwise_diff.reshape(cv.get_n_splits(X), repetitions, n_pairs)
    pairwise_diff_var = diff.var(axis=0, ddof=1).mean(axis=0)
    # compute statistics
    pairwise_diff_mean = pairwise_diff[0]
    pairwise_diff_std = np.sqrt(pairwise_diff_var)
    t_stats = pairwise_diff_mean / pairwise_diff_std
    df = repetitions
    p_vals = [t_distribution.sf(abs(t_stat), df)*2 for t_stat in t_stats]
    return _collect_dataframe(
        estimators, pairwise_diff_mean, pairwise_diff_std, t_stats, p_vals
    )