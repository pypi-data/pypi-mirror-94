"""# Utilities"""

import numpy as np
import pandas as pd
from sklearn.base import (
    BaseEstimator, RegressorMixin, 
    TransformerMixin as TransformerMixinBase
)


class TransformerMixin(TransformerMixinBase, BaseEstimator):
    """
    Version of scikit-learn's [`TransformerMixin`](https://scikit-learn.org/stable/modules/generated/sklearn.base.TransformerMixin.html) which implements a default inert `fit` method.
    """
    def fit(self, X, y=None):
        """
        This function doesn't do anything, but is necessary to include the transformer in a `Pipeline`.

        Returns
        -------
        self
        """
        return self
    
    def transform(self, X):
        """
        Must be implemented by the transformer.
        """
        raise NotImplementedError('Transfomer must implement transform method')


class ColumnSelector(TransformerMixin):
    """
    Selects columns from a dataframe.

    Parameters
    ----------
    columns : list
        List of columns to select.

    Examples
    --------
    ```python
    from fast_automl.utils import ColumnSelector

    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import make_pipeline

    X = pd.DataFrame({
    \    'x0': [-1, -2, 1, 2],
    \    'x1': [-1, -1, 1, 1]
    })
    y = np.array([1, 1, 2, 2])

    reg = make_pipeline(
    \    ColumnSelector(['x1']),
    \    LinearRegression()
    ).fit(X, y)
    reg.score(X, y)
    ```
    """
    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        """
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        
        y : optional, array-like of shape (n_samples, n_targets)
            Target values.

        Returns
        -------
        X or (X, y) : Where X columns have been selected
        """
        X = (
            X[self.columns] if isinstance(X, pd.DataFrame) 
            else X[:,self.columns]
        )
        return X if y is None else (X, y)


class ColumnRemover(TransformerMixin):
    """
    Removes columns from a dataframe.

    Parameters
    ----------
    columns : list
        List of columns to remove.

    Examples
    --------
    ```python
    from fast_automl.utils import ColumnRemover

    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import make_pipeline

    X = pd.DataFrame({
    \    'x0': [-1, -2, 1, 2],
    \    'x1': [-1, -1, 1, 1]
    })
    y = np.array([1, 1, 2, 2])

    reg = make_pipeline(
    \    ColumnRemover(['x0']),
    \    LinearRegression()
    ).fit(X, y)
    reg.score(X, y)
    ```
    """
    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        """
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        
        y : optional, array-like of shape (n_samples, n_targets)
            Target values.

        Returns
        -------
        X or (X, y) : Where X columns have been removed
        """
        X = (
            X.drop(columns=self.columns) if isinstance(X, pd.DataFrame)
            else np.delete(X, self.columns, axis=1)
        )
        return X if y is None else (X, y)


class BoundRegressor(RegressorMixin, BaseEstimator):
    """
    Constrains the predicted target value to be within the range of targets in
    the training data.

    Parameters
    ----------
    estimator : scikit-learn style regressor

    Attributes
    ----------
    estimator_ : scikit-learn style regressor
        Fitted regressor.

    y_max_ : scalar
        Maximum target value in training data.

    y_min_ : scalar
        Minimum target value in training data.

    Examples
    --------
    ```python
    from fast_automl.utils import BoundRegressor

    import numpy as np
    from sklearn.linear_model import LinearRegression

    X_train = np.array([
    \    [1, 2],
    \    [7, 8]
    ])
    X_test = np.array([
    \    [3, 4],
    \    [5, 1000]
    ])
    y_train = np.array([1.5, 7.5])
    y_test = np.array([3.5, 5.5])

    reg = LinearRegression().fit(X_train, y_train)
    reg.predict(X_test)
    ```

    Out:

    ```
    array([3.5, 7.5])
    ```
    """
    def __init__(self, estimator):
        self.estimator = estimator
        
    def fit(self, X, y, sample_weight=None):
        self.estimator_ = self.estimator.fit(X, y, sample_weight)
        self.y_min_, self.y_max_ = y.min(), y.max()
        return self
    
    def predict(self, X):
        y_pred = self.estimator_.predict(X)
        return np.clip(y_pred, self.y_min_, self.y_max_)