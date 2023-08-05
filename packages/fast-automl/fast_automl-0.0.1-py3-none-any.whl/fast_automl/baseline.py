"""# Baseline classifier and regressor"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils.validation import _check_sample_weight


class BaselineClassifier(ClassifierMixin, BaseEstimator):
    """
    Predicts the most frequent class.

    Attributes
    ----------
    classes_ : array-like of shape (n_classes,)
        A list of class weights known to the classifier.

    counts_ : array-like of shape (n_classes,)
        Normalized frequency of each class in the training data.

    dominant_class_ : int
        Class which appears most frequently in the training data.

    Examples
    --------
    ```python
    from fast_automl.baseline import BaselineClassifier

    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split

    X, y = load_digits(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
    clf = BaselineClassifier().fit(X_train, y_train)
    clf.score(X_test, y_test)
    ```
    """
    def fit(self, X, y, sample_weight=None):
        """
        Fit the model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.

        y : array-like of shape (n_samples,)
            Target values.

        sample_weight, array-like of shape (n_samples,), default=Noone
            Individual weights for each sample.

        Returns
        -------
        self
        """
        check_classification_targets(y)
        if sample_weight is None:
            self.classes_, self.counts_ = np.unique(y, return_counts=True)
        else:
            sample_weight = _check_sample_weight(sample_weight, X)
            sample_weight = sample_weight / sample_weight.mean()
            df = pd.DataFrame({'y': y, 'sample_weight': sample_weight})
            df = df.groupby('y').sum()
            self.classes_ = df.index.values
            self.counts_ = df.sample_weight.values
        self.counts_ = self.counts_ / self.counts_.sum()
        self.dominant_class_ = self.classes_[np.argmax(self.counts_)]
        return self
    
    def predict(self, X):
        """
        Predict class labels for samples in X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.

        Returns
        -------
        C : array of shape (n_samples,)
            Predicted class label for each sample.
        """
        return np.array([self.dominant_class_]*X.shape[0])
    
    def predict_proba(self, X):
        """
        Probability estimates.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Samples.

        Returns
        -------
        T : array-like of shape (n_samples, n_classes)
            Probability of the sample for each classes on the model, ordered by `self.classes_`.
        """
        return np.array([self.counts_]*X.shape[0])


class BaselineRegressor(RegressorMixin, BaseEstimator):
    """
    Predicts the mean target value.

    Attributes
    ----------
    y_mean_ : np.array
        Average target value.

    Examples
    --------
    ```python
    from fast_automl.baseline import BaselineRegressor

    from sklearn.datasets import load_boston
    from sklearn.model_selection import train_test_split

    X, y = load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    reg = BaselineRegressor().fit(X_train, y_train)
    reg.score(X_test, y_test)
    ```
    """
    def fit(self, X, y, sample_weight=None):
        """
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        
        y : array-like of shape (n_samples, n_targets)
            Target values.

        sample_weight, array-like of shape (n_samples,), default=Noone
            Individual weights for each sample.

        Returns
        -------
        self
        """
        sample_weight = _check_sample_weight(sample_weight, X)
        self.y_mean_ = (y * sample_weight).mean() / sample_weight.mean()
        return self
        
    def predict(self, X):
        """
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Samples.

        Returns
        -------
        C : array, shape (n_samples, n_targets)
            Predicted values
        """
        return self.y_mean_ * np.ones(shape=X.shape[0])