"""# Automated machine learning"""

from .cv_estimators import *
from .ensemble import (
    RFEVotingClassifierCV, RFEVotingRegressorCV, 
    StepwiseVotingClassifierCV, StepwiseVotingRegressorCV
)
from .metrics import check_scoring

import numpy as np
from sklearn.base import (
    BaseEstimator, ClassifierMixin, RegressorMixin, is_classifier
)
from sklearn.ensemble import VotingClassifier, VotingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

def make_cv_regressors():
    """
    Returns
    -------
    cv_regressors : list
        List of default CV regresssors.
    """
    return [
        RandomForestRegressorCV(),
        PCARandomForestRegressorCV(),
        LassoLarsCV(),
        PCALassoLarsCV(),
        RidgeCV(),
        PCARidgeCV(),
        ElasticNetCV(),
        PCAElasticNetCV(),
        KernelRidgeCV(),
        PCAKernelRidgeCV(),
        SVRCV(),
        PCASVRCV(),
        KNeighborsRegressorCV(),
        PCAKNeighborsRegressorCV(),
        AdaBoostRegressorCV(),
        PCAAdaBoostRegressorCV(),
        XGBRegressorCV(),
        PCAXGBRegressorCV()
    ]


def make_cv_classifiers():
    """
    Returns
    -------
    cv_classifiers : list
        List of default CV classifiers.
    """
    return [
        RandomForestClassifierCV(),
        PCARandomForestClassifierCV(),
        LogisticLassoCV(),
        PCALogisticLassoCV(),
        LogisticRidgeCV(),
        PCALogisticRidgeCV(),
        LogisticElasticNetCV(),
        PCALogisticElasticNetCV(),
        SVCCV(),
        PCASVCCV(),
        KNeighborsClassifierCV(),
        PCAKNeighborsClassifierCV(),
        AdaBoostClassifierCV(),
        PCAAdaBoostClassifierCV(),
        XGBClassifierCV(),
        PCAXGBClassifierCV()
    ]

class AutoEstimator(BaseEstimator):
    """
    Parameters
    ----------
    cv_estimators : list of CVEstimators, default=[]
        If an empty list, a default list of CVEstimators will be created.

    preprocessors : list, default=[]
        List of preprocessing steps before data is fed to the `cv_estimators`.

    ensemble_method : str, default='auto'
        If `'rfe'`, the ensemble is created using recursive feature 
        elimination. If `'stepwise'`, the ensemble is created using stepwise 
        addition. If `'auto'`, the ensemble is the better of the RFE and 
        stepwise ensemble methods.

    max_ensemble_size : int, default=50
        The maximum number of estimators to consider adding to the ensemble.

    n_ensembles : int, default=1
        Number of ensembles to create using different CV splits. These 
        ensembles get equal votes in a meta-ensemble.

    n_iter : int, default=10
        Number of iterations to run randomized search for the CVEstimators.

    n_jobs : int or None, default=None
        Number of jobs to run in parallel.

    verbose : bool, default=False
        Controls the verbosity.

    cv : int, cross-validation generator, or iterable, default=None
        Scikit-learn style cv parameter.

    scoring : str, callable, list, tuple, or dict, default=None
        Scikit-learn style scoring parameter. By default, a regressor 
        ensembles maximizes R-squared and a classifier ensemble maximizes ROC 
        AUC.

    Attributes
    ----------
    best_estimator_ : estimator
        Ensemble or meta-ensemble associated with the best CV score.
    """
    def __init__(
            self, cv_estimators=[], preprocessors=[], ensemble_method='auto', 
            max_ensemble_size=50, n_ensembles=1, n_iter=10, n_jobs=None, 
            verbose=False, cv=None, scoring=None
        ):
        if cv_estimators:
            self.cv_estimators = cv_estimators
        else:
            self.cv_estimators = (
                make_cv_classifiers() if is_classifier(self)
                else make_cv_regressors()
            )
        self.preprocessors = (
            preprocessors if isinstance(preprocessors, list) 
            else [preprocessors]
        )
        assert ensemble_method in ('auto', 'rfe', 'stepwise')
        self.ensemble_method = ensemble_method
        self.max_ensemble_size = max_ensemble_size
        self.n_ensembles = n_ensembles
        self.n_iter = n_iter
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.cv = cv
        self.scoring = scoring
        
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
        def fit_cv_estimator(i, est):
            if self.verbose:
                print('\nTuning estimator {} of {}: {}'.format(
                    i+1, len(self.cv_estimators), est.__class__.__name__
                ))
            est.fit(
                X, y, n_iter=self.n_iter, n_jobs=self.n_jobs, scoring=scoring
            )
            if self.verbose:
                print('Best estimator score: {:.4f}'.format(est.best_score_))

        def make_best_estimators():
            cv_results = [
                (res, est) 
                for est in self.cv_estimators 
                for res in est.cv_results_
            ]
            # create the best estimators
            # x[0][0] is the cv score
            best_params = sorted(
                cv_results, key=lambda x: x[0][0], reverse=True
            )[:self.max_ensemble_size]
            best_estimators = [
                est.make_estimator(**params) 
                for (_, params), est in best_params
            ]
            return [
                ('estimator {}'.format(i), estimator) 
                for i, estimator in enumerate(best_estimators)
            ]

        def build_ensemble(i):
            # build an ensemble of the best estimators
            if self.verbose:
                print(
                    '\nBuilding ensemble {} of {}'.format(
                        i+1, self.n_ensembles
                    )
                )
            ensemble_classes = []
            if self.ensemble_method in ('rfe', 'auto'):
                if is_classifier(self):
                    ensemble_classes.append(RFEVotingClassifierCV)
                else:
                    ensemble_classes.append(RFEVotingRegressorCV)
            elif self.ensemble_method in ('stepwise', 'auto'):
                if is_classifier(self):
                    ensemble_classes.append(StepwiseVotingClassifierCV)
                else:
                    ensemble_classes.append(StepwiseVotingRegressorCV)
            # TODO when ensemble_method is 'auto', both the RFE and stepwise estimators will have their sub-estimators make CV predictions, which is redundant work. A future release should get a CV split and make CV predictions here, then pass these to stepwise and RFE selection methods
            ensembles = [
                ensemble_cls(
                    best_estimators, n_jobs=self.n_jobs, cv=self.cv, scoring=scoring
                ).fit(X, y, sample_weight=sample_weight)
                for ensemble_cls in ensemble_classes
            ]
            ensemble = max(ensembles, key=lambda e: e.best_score_)
            if self.verbose:
                print('Best ensemble score: {:.4f}'.format(
                    ensemble.best_score_
                ))
            return 'ensemble {}'.format(i+1), ensemble.best_estimator_

        # store a copy of X to fit the best_estimator_
        X_copy = X.copy()
        for preprocessor in self.preprocessors:
            X = preprocessor.fit_transform(X)
        scoring = check_scoring(self.scoring, classifier=is_classifier(self))
        [fit_cv_estimator(i, est) for i, est in enumerate(self.cv_estimators)]
        best_estimators = make_best_estimators()
        ensembles = [
            build_ensemble(i) for i in range(self.n_ensembles)
        ]
        # if only one ensemble is built, there's no need to create a 
        # meta-ensemble
        # if multiple ensembles are built, give them an equal vote in a voting 
        # estimator
        if len(ensembles) == 1:
            meta_ensemble = ensembles[0][-1]
        elif is_classifier(self):
            meta_ensemble = VotingClassifier(ensembles, voting='soft')
        else:
            meta_ensemble = VotingRegressor(ensembles)
        self.best_estimator_ = make_pipeline(
            *self.preprocessors, meta_ensemble
        ).fit(X_copy, y)
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
        return self.best_estimator_.predict(X)
    
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
        return self.best_estimator_.predict_proba(X)


class AutoClassifier(ClassifierMixin, AutoEstimator):
    """
    Automatic classifier. Inherits from `AutoEstimator`.

    Examples
    --------
    ```python
    from fast_automl.automl import AutoClassifier

    from sklearn.datasets import load_digits
    from sklearn.model_selection import cross_val_score, train_test_split

    X, y = load_digits(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True, stratify=y)

    clf = AutoClassifier(ensemble_method='stepwise', n_jobs=-1, verbose=True).fit(X_train, y_train)
    print('CV score: {:.4f}'.format(cross_val_score(clf.best_estimator_, X_train, y_train).mean()))
    print('Test score: {:.4f}'.format(clf.score(X_test, y_test)))
    ```

    This runs for about 6-7 minutes and typically achieves a test accuracy of 
    96-99% and ROC AUC above .999.
    """


class AutoRegressor(RegressorMixin, AutoEstimator):
    """
    Automatic regressor. Inherits from `AutoEstimator`.

    Examples
    --------
    ```python
    from fast_automl.automl import AutoRegressor

    from sklearn.datasets import load_diabetes
    from sklearn.model_selection import cross_val_score, train_test_split

    X, y = load_diabetes(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=True)

    reg = AutoRegressor(n_jobs=-1, verbose=True).fit(X_train, y_train)
    print('CV score: {:.4f}'.format(cross_val_score(reg.best_estimator_, X_train, y_train).mean()))
    print('Test score: {:.4f}'.format(reg.score(X_test, y_test)))
    ```

    This runs for about 30 seconds and typically achieves a test R-squared of 
    .47-.53.
    """