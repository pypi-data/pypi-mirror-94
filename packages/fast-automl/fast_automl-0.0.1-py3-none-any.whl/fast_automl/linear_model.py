"""# Linear models"""

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge as RidgeBase


class ConstrainedLinearRegression(LinearRegression):
    """
    Linear regression where the coefficients are constrained to sum to a given 
    value.

    Parameters
    ----------
    constraint : scalar, default=0
        Sum of the regression coefficients.

    normalize : bool, default=False
    
    copy_Xbool, default=True
        If True, X will be copied; else, it may be overwritten.

    n_jobs : int, default=None
        The number of jobs to use for the computation. This will only provide speedup for n_targets > 1 and sufficient large problems. None means 1 unless in a joblib.parallel_backend context. -1 means using all processors.

    Attributes
    ----------
    coef_ : array-like of shape (n_features,) or (n_targets, n_features)
        Estimated coefficients for the linear regression contrained to sum to the given constraint value.

    Examples
    --------
    ```python
    from fast_automl.linear_model import ConstrainedLinearRegression

    from sklearn.datasets import load_boston
    from sklearn.model_selection import train_test_split

    X, y = load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True)
    reg = ConstrainedLinearRegression(constraint=.8).fit(X_train, y_train)
    print(reg.score(X_test, y_test))
    print(reg.coef_.sum())
    ```

    Out:

    ```
    0.6877629260102918
    0.8
    ```
    """
    def __init__(self, constraint=0, copy_X=True, n_jobs=None):
        self.constraint = constraint
        super().__init__(
            fit_intercept=False,
            copy_X=copy_X, 
            n_jobs=n_jobs
        )
        
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
        if X.shape[1] == 1:
            self.coef_ = np.array([self.constraint])
            return self
        if hasattr(X, 'values'):
            X = X.values
        X_0, X_rest = X[:,0], X[:,1:]
        X_rest = (X_rest.T - X_0).T
        y = y - self.constraint * X_0
        super().fit(X_rest, y, sample_weight)
        self.coef_ = np.insert(
            self.coef_, 0, self.constraint - self.coef_.sum()
        )
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
        return X @ self.coef_


class Ridge(RidgeBase):
    """
    Ridge regression with the option for custom prior weights on coefficients.

    Parameters
    ----------
    prior_weight : array-like of shape (n_features)
        Prior weight means.

    See [scikit-learn's ridge regression documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html) for additional parameter details.

    Attributes
    ----------
    coef_ndarray of shape (n_features,) or (n_targets, n_features)
        Weight vector(s).

    intercept_float or ndarray of shape (n_targets,)
        Independent term in decision function. Set to 0.0 if `fit_intercept = False`.

    Examples
    --------
    ```python
    from fast_automl.linear_model import Ridge

    from sklearn.datasets import load_boston
    from sklearn.model_selection import train_test_split

    X, y = load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True)
    reg = Ridge().fit(X_train, y_train)
    reg.score(X_test, y_test)
    ```
    """
    def __init__(
            self, alpha=1., prior_weight=0, normalize_coef=False, 
            fit_intercept=True, normalize=False, copy_X=True, max_iter=None, 
            tol=.001, solver='auto', random_state=None
        ):
        self.prior_weight = prior_weight
        self.normalize_coef = normalize_coef
        super().__init__(
            alpha, fit_intercept=fit_intercept, normalize=normalize, 
            copy_X=copy_X, max_iter=max_iter, tol=tol, solver=solver, 
            random_state=random_state
        )
        
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
        y = y - (self.prior_weight * X).sum(axis=1)
        super().fit(X, y, sample_weight)
        if self.normalize_coef:
            self.coef_ -= self.coef_.mean()
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
        return super().predict(X) + (self.prior_weight * X).sum(axis=1)