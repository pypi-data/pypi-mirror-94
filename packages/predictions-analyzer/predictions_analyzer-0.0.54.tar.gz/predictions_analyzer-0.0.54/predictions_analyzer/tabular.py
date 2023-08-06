"""
For Tabular_ML Predictions.

This serves to simulate the data and API of the tabular_prediction_analyzer.

For now, it is the main module for the tabular ML analyzer and just
serves as an example of what is possible.

Should inherit a Base Class Analyzer in the future that users can
use with real numpy or pandas data.

"""
from tqdm import tqdm
from time import time



from lightgbm import LGBMClassifier
import xgboost as xgb

import sklearn.dummy
import sklearn.datasets
import sklearn.linear_model
import sklearn.tree
import sklearn.ensemble
import sklearn.metrics
from sklearn.metrics import plot_confusion_matrix, classification_report
import sklearn.model_selection

import sklearn.multioutput

import sklearn.feature_selection

import sklearn.naive_bayes
import sklearn.neighbors

from sklearn.utils.multiclass import unique_labels

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from predictions_analyzer.analyze import Analyzer

from itertools import combinations

# Put this in an if-statement?
# By Extension?
# How to extend this without 'requiring it' if the user
# Doesn't use it?
import wandb


def get_classification(random_state = 42):
    """
    Creates a classification dataset.
    Wrapper for sklearn's make_classification.

    :param random_state: Specifies a random seed
    :return: A tuple of X,y values.
    """
    X, y = sklearn.datasets.make_classification(
        n_samples = 1000,
        n_classes = 5,
        n_features = 20,
        n_informative = 5,
        n_redundant = 15,
        n_clusters_per_class = 3,
        random_state = random_state
    )

    # For logging
    print(X.shape)
    print(y.shape)

    return X, y

class BaseAnalyzer:
    """
    Contains methods common to both regression and classification
    analyzers.

    """


    def show_models(self):
        for model in self.models:
            print("\n")
            print(model)

    def remove_model(self):
        """

        :return:
        """
        pass

    def update_model(self):
        pass

    def add_model(self, model_name:str, model_object):
        """
        Adds a model
        :param model_name: classifier_name
        :param model_obj: classifier object with .fit and .predict methods
        :return:

        """

        # Is this possible?
        # self.model_name = model_object

        self.models.append((model_object, model_name))

    def add_models(self):
        """
        Plural version of add_model
        Eventually refactor into one function

        :return:

        """
        pass

    def remove_all_models(self):
        pass

    def restore_baseline_models(self):
        self._initialize_models()

    def _initialize_preds(self):
        self.ensembled_preds_df = pd.DataFrame()

        # This will be the original_preds & ensembled_preds
        self.all_preds_df = pd.DataFrame()

    def _set_is_fit(self, is_it_fit: bool):
        """
        Sets if the estimators are fit_models or not
        :return:
        """

        self.is_fit = is_it_fit

    def _is_fit(self):
        """
        TO DO - Make This Private

        find if the models are fit_models or not.
        This can be updated if there is a better method.
        :return:
        """

        if self.is_fit == False:
            return False
        if self.is_fit == True:
            return True

    def load_unsplit_data(self, X, y):

        # In case it is a numpy array.
        try:
            self.feature_names = X.columns
        except:
            pass

        # In case it is a numpy array.
        try:
            self.target_names = y.columns
        except:
            pass

        self.X = X
        self.y = y

        #self.is_multioutput = self.y.shape[1] > 1
        #print("is multioutput: ", self.is_multioutput)

    def load_split_data(self, X_train, y_train,
                        X_valid, y_valid):

        self.X_train = X_train
        self.y_train = y_train
        self.X_valid = X_valid
        self.y_valid = y_valid

    def fit_predict_cv(self, cv, verbose = True):
        """
        This method uses a specified cross validation method to fit
        and predict.

        :param verbose:
        :param cv:
        :return:
        """

    def fit_linear(self):
        pass

    def fit_trees(self):
        pass

    def fit_nonparametric(self):
        pass

    def fit_models(self, verbose = True):
        """
        Fit all models on the self.X_train and self.y_train data.
        Should only be used if you don't already have
        offline predictions done already.

        :return:
        """

        #TODO Calls _fit?

        self.model_fit_speeds = pd.DataFrame()

        for model, model_name in self.models:

            time_start = time()

            model.fit(self.X_train, self.y_train)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            if verbose:
                print("fit:", model_name, time_to_fit, "seconds")

            self.model_fit_speeds[model_name] = time_to_fit


        self.is_fit = self._set_is_fit(True)

    def predict(self,
                verbose = True,
                ):
        """
        Predict on the self.X_valid and self.y_valid and save time metrics.
        Must run or load a validation split and .fit_models first.

        :param verbose:
        :return:
        """

        # TODO: Calls _predict

        # Here or in the __init__?
        self.preds_df = pd.DataFrame(self.y_true, columns = ["y_true"])

        # TODO: Check if model split_val_train has been called

        self.model_pred_speeds = pd.DataFrame()

        for model, model_name in self.models:

            time_start = time()

            # TODO: Add Exception handling to predict doesn't stop.

            self.preds_df[model_name] = model.predict(self.X_valid)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            if verbose:
                print("predicted with:", model_name, "took ", time_to_fit, "seconds")

            self.model_pred_speeds[model_name] = time_to_fit

        # Drop y_true.  Just keep it in self.y_true
        self.preds_df = self.preds_df.drop("y_true", axis = 1)

        return self.preds_df

    def initialize_wandb(self,
                   project_name:str = None,
                   group_name:str = None,
                   experiment_name:str = None
                   ):
        """
        This initializes weights and biases project, group, and
        experiment names to the Analyzer object.

        :param project_name:
        :param group_name:
        :param experiment_name:
        :return:
        """

        self.project_name = project_name
        self.experiment_name = experiment_name
        self.group_name = group_name

        wandb.init(project = project_name,
                  group = group_name,
                  name = experiment_name)


    def wandb_sklearn_log(self):
        pass

    def log_stats_with_wandb(self):
        # TODO: Put this in BaseAnalyzer

        pass

    def information_analysis_with_wandb(self):
        # TODO: Put this in BaseAnalyzer

        pass

    def feature_analysis_with_wandb(self):
        # TODO: Put this in BaseAnalyzer
        # All feature selector information
        # Statistical tests for features... outputs for analysis.
        # Correlations and their meaning.
        # Several models with feature importance
        # Intersection of features
        # Union of best features above threshold.

        pass

    def _store_column_names(self):
        pass

    def _fit_initialize_logs(self):
        pass

    def _fit_initialize_wandb(self,
                              model_name,
                              reinit = True):

        wandb.init(project=self.project_name,
                   group=self.group_name,
                   name=model_name,
                   reinit=reinit)

    def _fit_initialize_preds(self):
        """
        Private function to internally initialize preds object and other
        prediction state objects.

        predict_proba objects, etc.

        :return:
        """
        # Check if self.project_name is not None. etc.
        print(self.project_name, self.group_name, self.experiment_name)

        ########### Check this.
        # Here or in the __init__?
        self.preds_df = pd.DataFrame(self.y_true, columns=["y_true"])

        # Drop y_true.  Just keep it in self.y_true
        self.preds_df = self.preds_df.drop("y_true", axis=1)
        ############

        self.model_fit_speeds = pd.DataFrame()
        self.model_pred_speeds = pd.DataFrame()

        y_labels = unique_labels(self.y_valid)


    def _fit_model(self,
                   model,
                   model_name,
                   use_wandb = False,
                   verbose = True,
                   tags = ["untagged"]):

        # Have VERBOSE be an object setting.

        print(model_name)

        self._fit_initialize_wandb(model_name)

        time_start = time()

        model.fit(self.X_train, self.y_train)

        time_finish = time()
        time_to_fit = round(time_finish - time_start, 4)

        # TODO: Log with Tags
        if use_wandb:
            wandb.log({"fit_time":time_to_fit})

        if verbose:
            print("fit:", model_name, time_to_fit, "seconds")

        self.model_fit_speeds[model_name] = time_to_fit

    def _predict_model(self,
                       use_wandb = False,
                       multioutput = False,
                       aggregation = None):
        """

        :param use_wandb:
        :param multioutput: True, False, "Auto" <-- Change to static typing if adding auto.....
        :param aggregation: If multi-output, shouldl you aggregate the predictions?
        :return:
        """

        pass

    def _wandb_log_probas(self):
        pass

    def _wandb_log_classification_metrics(self):
        pass

    def _wandb_log_feature_importances(self):
        pass

    def _fit_predict_log_wandb_loop(self,
                                   model,
                                   model_name,
                                   predict_probas = True,
                                   do_class_metrics = True,
                                   do_feature_importances = True):

        # REFACTOR LIKE THIS:
        #self._fit_model(model, model_name, use_wandb=True)
        #self._predict_model()
        #self._wandb_log_probas()
        #self._wandb_log_classification_metrics()
        #self._wandb_log_feature_importances()

        pass

    def fit_predict_log_wandb_multi(self,
                                    verbose = True):
        """
        TODO: Use DRY design to update this and the not-multi
        version of this function.

        :return:
        """

        # Refactor like this:
        # for model, model_name in self.models:
        #    print(model_name)
        #    self._fit_predict_log_wandb_loop(model, model_name)


        #########OLD But Working##########
        # Check if self.project_name is not None. etc.
        print(self.project_name, self.group_name, self.experiment_name)

        ########### Check this.
        # Here or in the __init__?
        self.preds_df = pd.DataFrame(self.y_true, columns=["y_true"])

        # Drop y_true.  Just keep it in self.y_true
        self.preds_df = self.preds_df.drop("y_true", axis=1)
        ############

        self.model_fit_speeds = pd.DataFrame()
        self.model_pred_speeds = pd.DataFrame()

        # TODO: FIX BUG WHERE LABELLING MULTICLASS COMES OUT WRONG
        # self.y_valid[:100]
        y_labels = unique_labels(self.y_valid)

        # y_labels = [0,1]  # TODO: Temp fix FOR JS

        print("y_labels: ", y_labels)

        """

        wandb.sklearn.plot_class_proportions(self.y_train,
                                             self.y_valid,
                                             labels=y_labels)
        """

        for model, model_name in self.models:

            print(model_name)

            wandb.init(project=self.project_name,
                       group=self.group_name,
                       name=model_name,
                       reinit=True)

            time_start = time()

            model.fit(self.X_train, self.y_train)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            wandb.log({"fit_time": time_to_fit})

            if verbose:
                print("fit:", model_name, time_to_fit, "seconds")

            self.model_fit_speeds[model_name] = time_to_fit

            ######

            # TODO: Check if model split_val_train has been called

            time_start = time()

            # TODO: Add Exception handling to predict doesn't stop.

            # TODO: Make Multi Compatible
            this_preds = model.predict(self.X_valid)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            # TODO: Add TRAINING Accuracy as well as Validation accuracy.
            # TODO: Add difference in training and validation accuracy.
            # TODO: Do this for all metrics?

            if verbose:
                print("predicted with:", model_name, "took ", time_to_fit, "seconds")

            wandb.log({"predict_time": time_to_fit})

            # self.model_pred_speeds[model_name] = time_to_fit

            # TODO: Add - model.predict_proba(self.X_valid)

            wandb.sklearn.plot_learning_curve(model, self.X_train, self.y_train)

            # TODO: Name this correctly.  It isn't an ROC thing.
            can_plot_roc = ["logistic_l1", "logistic_l2"]
            cannot_plot_roc = ["ridge", "bagged_svc_clf"]

            if model_name in cannot_plot_roc:
                pass
            else:
                predicted_probas = np.array(model.predict_proba(self.X_valid))

                print("probas shape:", predicted_probas.shape)
                print("valid shape", self.y_valid.shape)

                #this_roc_score = sklearn.metrics.roc_auc_score(
                #    y_true = self.y_valid,
                #    y_score = predicted_probas
                #)

                #wandb.log({"roc_auc_score": this_roc_score})

                #this_roc_curve = sklearn.metrics.plot_roc_curve(model,
                #                                    self.X_valid,
                #                                    self.y_valid,
                #                                    response_method = "predict_proba")

                # wandb.log({model_name+"roc":this_roc_curve})


                #wandb.sklearn.plot_precision_recall(self.y_valid,
                #                                    predicted_probas,
                #                                    labels=y_labels)

            #wandb.sklearn.plot_confusion_matrix(self.y_valid,
            #                                    self.preds_df[model_name],
            #                                    labels=y_labels)

            #this_acc = sklearn.metrics.accuracy_score(self.y_valid,
            #                                          self.preds_df[model_name])

            this_model_score = model.score(self.X_valid, self.y_valid)
            wandb.log({"accuracy_score": this_model_score})

            #this_bal_acc = sklearn.metrics.balanced_accuracy_score(self.y_valid,
            #                                                       self.preds_df[model_name])

            #wandb.log({"balanced_accuracy": this_bal_acc})
            """
            try:
                this_recall = sklearn.metrics.recall_score(self.y_valid,
                                                           self.preds_df[model_name])
                wandb.log({"recall_score": this_recall})
            except:
                print("skipping recall for", model_name)

            try:
                this_precision = sklearn.metrics.precision_score(self.y_valid,
                                                                 self.preds_df[model_name])
                wandb.log({"precision_score": this_precision})
            except:
                print("skipping precision for", model_name)

            cannot_feature_importance = ["dummy_prior_clf", "nb"]
            if model_name in cannot_feature_importance:
                pass
            else:
                wandb.sklearn.plot_feature_importances(model,
                                                       list(self.X_valid.columns))
            """


    def fit_predict_log_wandb(self,
                              verbose = True):
        """
        Fits, Predicts, and Logs all classifiers with
        Weights and Biases


        :return:
        """

        # Check if self.project_name is not None. etc.
        print(self.project_name, self.group_name, self.experiment_name)

        ########### Check this.
        # Here or in the __init__?
        self.preds_df = pd.DataFrame(self.y_true, columns=["y_true"])

        # Drop y_true.  Just keep it in self.y_true
        self.preds_df = self.preds_df.drop("y_true", axis=1)
        ############

        self.model_fit_speeds = pd.DataFrame()
        self.model_pred_speeds = pd.DataFrame()

        y_labels = unique_labels(self.y_valid)

        """
        
        wandb.sklearn.plot_class_proportions(self.y_train,
                                             self.y_valid,
                                             labels=y_labels)
        """

        for model, model_name in self.models:

            print(model_name)

            wandb.init(project=self.project_name,
                       group=self.group_name,
                       name=model_name,
                       reinit=True)

            time_start = time()

            model.fit(self.X_train, self.y_train)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            wandb.log({"fit_time":time_to_fit})

            if verbose:
                print("fit:", model_name, time_to_fit, "seconds")

            self.model_fit_speeds[model_name] = time_to_fit

            ######

            # TODO: Check if model split_val_train has been called

            time_start = time()

            # TODO: Add Exception handling to predict doesn't stop.

            self.preds_df[model_name] = model.predict(self.X_valid)

            time_finish = time()
            time_to_fit = round(time_finish - time_start, 4)

            # TODO: Add TRAINING Accuracy as well as Validation accuracy.
            # TODO: Add difference in training and validation accuracy.
            # TODO: Do this for all metrics?

            if verbose:
                print("predicted with:", model_name, "took ", time_to_fit, "seconds")

            wandb.log({"predict_time": time_to_fit})

            self.model_pred_speeds[model_name] = time_to_fit

            # TODO: Add - model.predict_proba(self.X_valid)

            wandb.sklearn.plot_learning_curve(model, self.X_train, self.y_train)

            #TODO: Name this correctly.  It isn't an ROC thing.
            can_plot_roc = ["logistic_l1", "logistic_l2"]
            cannot_plot_roc = ["ridge", "bagged_svc_clf"]

            if model_name in cannot_plot_roc:
                pass
            else:
                predicted_probas = model.predict_proba(self.X_valid)

                wandb.sklearn.plot_roc(self.y_valid,
                                       predicted_probas,
                                       labels = y_labels)

                wandb.sklearn.plot_precision_recall(self.y_valid,
                                                   predicted_probas,
                                                   labels = y_labels)

            wandb.sklearn.plot_confusion_matrix(self.y_valid,
                                                self.preds_df[model_name],
                                                labels = y_labels)

            this_acc = sklearn.metrics.accuracy_score(self.y_valid,
                                                      self.preds_df[model_name])
            wandb.log({"accuracy_score":this_acc})

            this_bal_acc = sklearn.metrics.balanced_accuracy_score(self.y_valid,
                                                                   self.preds_df[model_name])

            wandb.log({"balanced_accuracy": this_bal_acc})

            try:
                this_recall = sklearn.metrics.recall_score(self.y_valid,
                                                           self.preds_df[model_name])
                wandb.log({"recall_score": this_recall})
            except:
                print("skipping recall for", model_name)

            try:
                this_precision = sklearn.metrics.precision_score(self.y_valid,
                                                           self.preds_df[model_name])
                wandb.log({"precision_score": this_precision})
            except:
                print("skipping precision for", model_name)


            cannot_feature_importance = ["dummy_prior_clf", "nb"]
            if model_name in cannot_feature_importance:
                pass
            else:
                wandb.sklearn.plot_feature_importances(model,
                                                       list(self.X_valid.columns))



            """
            wandb.sklearn.plot_classifier(model,
                                          self.X_train,
                                          self.X_valid,
                                          self.y_train,
                                          self.y_valid,
                                          y_pred = self.preds_df[model_name],
                                          y_probas = model.predict_proba(self.X_valid),
                                          labels = unique_labels(self.y_valid),
                                          model_name=model_name,
                                          feature_names=self.X_train.columns)
            """


    def tune_with_optuna(self, trials = 20):
        """
        This method will tune
        :param trials:
        :return:
        """
        pass


    def apply_ytrue(self,
                       func,
                       df: pd.DataFrame = None,
                       func_name: str = None,):
        """
        TO UPDATE: Should be private function

        Applies func(y_true, col in cols...) across dataframe df

        Helper function to use df.apply with
        self.preds_df and self.y_true

        func - the function being passed to apply
        across columns.  func should take self.y_true
        as its first argument.

        df - the df to apply the func to.

        :return: a df or series with the result.
        """

        # How to get this to work with pd.apply when there is varying
        # positional arguments?  args = () ?

        if df is None:
            df = self.preds_df

        applied_df = pd.DataFrame(columns = df.columns,
                                  index = [func_name])

        for col in df.columns:
            applied_df[col] = func(self.y_true, df[col])

        return applied_df

    def add_to_metrics_from_ytrue_and_preds_df(self,
                                               func,
                                               func_name: str = None):
        """

        Helper wrapper function to apply_ytrue
        encapsulate any future
        changes to apply_ytrue or the
        preds_df structure

        :return:
        """

        # FIX: apply_ytrue should be private function
        # Modularize this.
        ### DRY Violated

        new_metric = self.apply_ytrue(func = func,
                                      df = self.preds_df,
                                      func_name = func_name)

        assert new_metric.empty != True  # Was the new_metric created?

        # Encapsulate this in a new private function
        self.metrics_df = pd.concat([self.metrics_df, new_metric])
        assert self.metrics_df.empty != True  # Has metric been added to self.metrics_df?


        ########### Do the same for Ensembled Preds ###################
        # Modularize this
        # If ensembled predictions have been created...
        if self.ensembled_preds_df.empty != True:
            new_ensembled_metric = self.apply_ytrue(func = func,
                                                    df=self.ensembled_preds_df,
                                                    func_name=func_name)

            self.metrics_df = pd.concat([self.metrics_df, new_ensembled_metric])

            assert self.metrics_df.empty != True  # Has metric been added to self.metrics_df?

    def extract_best_feature_importances(self):
        pass

    def extract_n_best_features(self):
        pass

    def show_permutation_importances(self):
        pass




class BaseClassificationAnalyzer(BaseAnalyzer):
    """
    Base class for all Classification Analyzers

    """

    def _initialize_dummy_models(self):
        pass


    def _initialize_linear_models(self):
        self.logistic_reg = sklearn.linear_model.LogisticRegression(penalty="none",
                                                                    n_jobs=self.n_jobs,
                                                                    max_iter=1000,
                                                                    random_state=self.random_state)

        self.logistic_l1 = sklearn.linear_model.LogisticRegression(penalty="l1",
                                                                   solver="saga",
                                                                   n_jobs=self.n_jobs,
                                                                   max_iter=1000,
                                                                   random_state=self.random_state)

        self.logistic_l2 = sklearn.linear_model.LogisticRegression(penalty="l2",
                                                                   solver="saga",
                                                                   n_jobs=self.n_jobs,
                                                                   max_iter=1000,
                                                                   random_state=self.random_state)

        self.logistic_elastic = sklearn.linear_model.LogisticRegression(penalty="elasticnet",
                                                                        solver="saga",
                                                                        l1_ratio=0.5,
                                                                        n_jobs=self.n_jobs,
                                                                        max_iter=1000,
                                                                        random_state=self.random_state)

        self.ridge = sklearn.linear_model.RidgeClassifier(normalize=True,
                                                          random_state=self.random_state)

        self.linear_models = [
            (self.logistic_reg, "logistic_reg"),
            (self.logistic_l1, "logistic_l1"),
            (self.logistic_l2, "logistic_l2"),
            (self.ridge, "ridge"),
        ]

    def _initialize_tree_models(self):
        self.dec_tree = sklearn.tree.DecisionTreeClassifier(max_depth=self.max_depth,
                                                            random_state=self.random_state)

        self.extr_tree = sklearn.ensemble.ExtraTreesClassifier(max_depth=self.max_depth,
                                                               n_jobs=self.n_jobs,
                                                               random_state=self.random_state)

        self.random_forest = sklearn.ensemble.RandomForestClassifier(max_depth=self.max_depth,
                                                                     n_jobs=self.n_jobs,
                                                                     random_state=self.random_state)

        self.bagging_dt_clf = sklearn.ensemble.BaggingClassifier(max_features=0.8,
                                                                 max_samples=self.use_subsample,
                                                                 n_jobs=self.n_jobs,
                                                                 random_state=self.random_state)

        self.bagging_svc_clf = sklearn.ensemble.BaggingClassifier(
            base_estimator=sklearn.svm.SVC(random_state=self.random_state,
                                           ),
            max_features=0.8,
            max_samples=self.use_subsample,
            n_jobs=self.n_jobs,
            random_state=self.random_state
            )

        self.xgb_clf = xgb.XGBClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            subsample=self.use_subsample,
            tree_method="approx",
            random_state=self.random_state
        )

        self.lgb_clf = LGBMClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            num_leaves=64,
            random_state=self.random_state
        )

        self.tree_models = [
            (self.dec_tree, "dec_tree"),
            (self.extr_tree, "extr_tree"),
            (self.bagging_dt_clf, "bagged_dt_clf"),
            (self.bagging_svc_clf, "bagged_svc_clf"),
            (self.xgb_clf, "xgb_clf"),
            (self.lgb_clf, "lgb_clf")
        ]

    def _initialize_nonparametric_models(self):
        self.svc = sklearn.svm.SVC(random_state=self.random_state,
                                   probability=True)

        self.nb = sklearn.naive_bayes.GaussianNB()
        self.nb_complement = sklearn.naive_bayes.ComplementNB()

        self.knn = sklearn.neighbors.KNeighborsClassifier()

    def _initialize_stacked_models(self):
        pass

    def _initialize_voting_models(self):
        pass

    def _initialize_model_groups(self):
        # TODO: Organize into model types so each model can .fit on data made for it.
        # Logistic, Linear classifiers. SVC. KNN.
        self.models_that_need_scaled_data = []

        # Don't use these with big-data.   KNN or SVC.
        self.models_that_dont_scale_well = [
            (self.svc, "SVC"),
            (self.knn, "knn"),
            (self.random_forest, "random_forest")
        ]

        # A list of named tuples of all models to loop through.
        self.models = [
            (self.dummy, "dummy_prior_clf"),
            (self.logistic_reg, "logistic_reg"),
            (self.logistic_l1, "logistic_l1"),
            (self.logistic_l2, "logistic_l2"),
            (self.ridge, "ridge"),
            (self.svc, "SVC"),
            (self.nb, "nb"),
            (self.dec_tree, "dec_tree"),
            (self.extr_tree, "extr_tree"),
            (self.bagging_dt_clf, "bagged_dt_clf"),
            (self.bagging_svc_clf, "bagged_svc_clf"),
            (self.xgb_clf, "xgb_clf"),
            (self.lgb_clf, "lgb_clf")
        ]

    def _make_models_multioutput(self):

        i = 0
        for model, model_name in self.models:
            print("Converting", model_name, "to multioutput")

            self.models[i] = (sklearn.multioutput.MultiOutputClassifier(model), model_name)

            i += 1

        self.show_models()

    def _initialize_models(self,
                           multioutput = False):
        """

        :param multioutput: Whether to make all models multioutput models.
        :return:
        """

        # TODO: Add Multiple Dummy Baselines
        self.dummy = sklearn.dummy.DummyClassifier(strategy="prior")

        # Set random state / seeds for these

        self._initialize_linear_models()
        self._initialize_nonparametric_models()
        self._initialize_tree_models()
        self._initialize_model_groups()

        if self.is_multi_output:
            self._make_models_multioutput()

    def _initialize_metrics(self):

        self.metrics_df = pd.DataFrame()
        self.accuracy = []  # List of accuracy scores?

        self.binary_metrics = [
            (sklearn.metrics.accuracy_score, "accuracy_score"),
            (sklearn.metrics.roc_auc_score, "roc_auc_score")
        ]

        self.binary_or_multiclass_metrics = [
            (sklearn.metrics.precision_score, "precision_score"),
            (sklearn.metrics.recall_score, "recall_score"),
            (sklearn.metrics.f1_score, "f1_score"),
            (sklearn.metrics.log_loss, "log_loss")

        ]

    def generate_data(self):
        X, y = get_classification(random_state=self.random_state)
        X = pd.DataFrame(X)
        y = pd.DataFrame(y)

        # TODO: Delete this to not duplicate data.  Just deal with train/val splits.
        self.X = X
        self.y = y

        self.split_val_train()

    def stack_classifiers(self):
        # TODO: Damn!  The tuple is the in the reverse order!!!

        self.stacking_clf = sklearn.ensemble.StackingClassifier(self.models)


    def model_feature_sklearn_loop(self):
        pass

    def show_feature_analysis_from_model(self):

        colnames = self.X.columns

        xgb_selector = sklearn.feature_selection.SelectFromModel(self.xgb_clf,
                                                                 prefit=True)

        xgb_selected = xgb_selector.transform(self.X)
        print(xgb_selected.shape)

        # xgb_selected_df = None

        xgb_support = xgb_selector.get_support()
        print(xgb_support)

        xgb_threshold = xgb_selector.threshold_
        print(xgb_threshold)


    def show_feature_analysis(self):


        pass


class BaseRegressionAnalyzer(BaseAnalyzer):
    pass

class ClassificationAnalyzer(BaseClassificationAnalyzer):
    """
    FITTING
    PREDICTING
    ANALYZING should be clearly differentiated and encapsulated things.

    """

    def __init__(self,
                 random_state = 42,
                 max_depth = 5,
                 n_estimators = 100,
                 use_subsample = 0.8,
                 n_jobs = -1,
                 simulate_data = False,  # TODO: This feels strange here.
                 multi_output = False):  # TODO: Make automatic

        self.random_state = random_state

        self.n_estimators = n_estimators
        self.use_subsample = use_subsample

        self.max_depth = max_depth
        self.is_fit = False
        self.n_jobs = n_jobs

        self.is_multi_output = multi_output

        self._initialize_models()
        self._initialize_metrics()
        self._initialize_preds()

        if simulate_data:
            self.generate_data()


    def _update_validation_ready_models(self):
        """
        Models with early stopping should include validation sets.

        :return:
        """
        pass

    def split_val_train(self,
                        train_fraction = 4/5,
                        method = "stochastic",
                        verbose = True,
                        ):
        """
        Splits data into train and validation splits.
        Useful for quick processing.

        :param X:
        :param y:
        :param: method ("stochastic", "time_series", "groupkfold", "multi_stochastic")
        :return:
        """

        X = self.X
        y = self.y

        length_of_X = len(X)

        if method == "stochastic":
            self.X_train, self.X_valid, self.y_train, self.y_valid = sklearn.model_selection.train_test_split(
                X, y, train_size = train_fraction,
                stratify = y,
                random_state=self.random_state,
                shuffle = True
            )

        if method == "time_series":
            # TODO: Add stochastic and time-series variants.

            split_at_id = int(length_of_X * train_fraction)

            self.X_train = X.iloc[0:split_at_id, :]
            self.y_train = y.iloc[0:split_at_id]

            self.X_valid = X.iloc[split_at_id:, :]
            self.y_valid = y.iloc[split_at_id:]

        if method == "multi_stochastic":
            self.X_train, self.X_valid, self.y_train, self.y_valid = sklearn.model_selection.train_test_split(
                X, y, train_size=train_fraction,
                random_state=self.random_state,
                shuffle=True
            )

        self.y_true = self.y_valid
        self._update_validation_ready_models()

    def cross_validate(self):
        pass


    def load_preds(self):
        pass


    def within_threshold(self, threshold: float):
        """
        Finds all
        :param threshold: float - Find all outputs that are within a threshold.

        :return:
        """

        # Validate that the model is fit_models already.


    def show_preds_report(self, save = False):
        """
        Show pandas styled dataframe with reds -> incorrect, greens -> correct.

        Sort by number incorrect. / TODO: customize show features.

        Classification Report for Each Classifier.

        :param save: Save outputs to a filepath.

        :return:
        """
        pass


    def show_confusion_matrix(self, verbose = True):

        for model, model_name in tqdm(self.models):

            # TODO: Add Exception handling to predict doesn't stop.

            disp = plot_confusion_matrix(model,
                                  self.X_valid,
                                  self.y_true,
                                  cmap = plt.cm.Blues)

            plt.title("Confusion Matrix For: " + model_name)
            plt.show()


    def show_classification_report(self):

        for col in self.preds_df.columns:

            clf_report = classification_report(self.y_true, self.preds_df.loc[:,col], output_dict=True)
            clf_report_print = classification_report(self.y_true, self.preds_df.loc[:, col])

            print("\n\n" + col)
            print(clf_report_print)
            sns.heatmap(pd.DataFrame(clf_report).T,
                        annot = True, vmin = 0, vmax = 1,
                        cmap = plt.cm.Blues)

            plt.title("Classification Report for: " + col)
            plt.show()


    def explore_feature_distributions(self):
        pass

    def explore_statistics_for_hardest(self):
        """
        This function checks out the z-scores
        and other important statistics
        for each of the hardest

        :return:
        """
        pass

    def explore_features_for_hardest(self):
        """
        Checks out each feature and color codes the
        'hardest' to categorize - seeing if the harder
        samples have anything in common
        feature-wise.


        Displays feature distributions with sample
        difficulty coded ordinally.

        :return:
        """
        pass
    def show_best_recall(self):
        pass

    def show_best_precision(self):
        pass

    def show_best_f1(self):
        pass

    def show_best_on_hardest_samples(self):
        pass

    def show_confidence_on_hardest_samples(self):
        pass

    def get_best_on_particular_rows(self):
        pass

    def ensemble_analysis(self):
        # Which ensemble gives the best results?

        # Create different combinations of all the preds
        # Add the ensembles to the confusion matrices / classification reports!
        # Voting classifiers
        # Stacking Classifiers
        # Mean and Median Classifiers

        pass

    def show_all_reports(self):

        for col, model in zip(self.preds_df.columns, self.models):

            assert(model[1] == col)  # The column name must equal the model name

            # plt.subplots - Confusion matrix and Classification report
            # Speed

        # Overall Reports:
        # Best Precision
        # Best Recall
        # Best f1 Score.
        # Best Accuracy.

        # Diversity Analysis.


    def do_binary_metrics(self):
        pass

    def get_num_wrong_right(self):
        """

        :return: a df of number right, wrong, and proportions
        """

        num_rightwrong_df = pd.DataFrame()


    def fit_accuracy_scores(self):
        """
        Redundant function now?
        Remove?

        :return:
        """

        self.add_to_metrics_from_ytrue_and_preds_df(
            func=sklearn.metrics.accuracy_score,
            func_name="accuracy_score")


    def get_classification_metrics(self):

        """
        ANALYZE: assumes fit_predicted data already
        and just needs self.preds_df.

        Get classification_metrics for each of the classifiers

        :return:
        """
        # Call helper function to find if this is a multi-class problem
        # or a binary classification problem.

        # Make this configurable
        multiclass_kwargs = {"average":"micro"}

        metric_names = ["accuracy", "recall_score", "precision_score", "f1_score"]

        self.metrics_df = pd.DataFrame(index = metric_names)

        # Need a better way to do this!!!!!!!!!
        # Nested for loop?  Apply?

    def analyze(self):
        pass

    def show_decision_regions(self):
        pass

    def find_hardest_samples(self):
        """
        ANALYZE:

        These are the samples that were the hardest to
        get correct.

        For each sample, find total "correct" and "wrong"
        Sort these results by the most wrong.

        FOLLOW UP:
        Then do a cluster / correlation / dependency analysis
        in the X field on these samples to find out
        if they have something in common.

        # TODO: Add predict_proba and sort the smallest probabilities.
        # TODO: Show decision regions.  Above function.
        # TODO: Add just support_vectors as these are the closest to the decision boundaries.  X[svm.support_]

        :return:
        """

        trues_df = self.preds_df.copy()

        # Set all to the trues for easy comparison.
        for col in trues_df.columns:
            trues_df[col] = self.y_true

        correct_mask = trues_df == self.preds_df


        self.correct_mask = correct_mask

        n_correct = correct_mask.sum(axis = 1)

        mask_with_margins = correct_mask.insert(0, "n_clf_correct", n_correct)

        # TODO: This doesn't do what I want.  It is still set to "correct_mask"
        self.correct_mask_with_margins_ = mask_with_margins

        n_correct = n_correct.sort_values()
        self.hardest_samples_ = n_correct

        print("\nSorted Hardest Samples: retrievable with the .hardest_samples_ attribute")
        print("Key is row index of sample, Value is the number of correct from all predictors")
        print(n_correct)

        self.n_freq_correct = n_correct.value_counts().sort_values()

        print("\nNumber of correct: retrievable with the .n_freq_correct attribute_")
        print("Index is the number of correct predictions, value is how many samples had that number of correct")
        print(self.n_freq_correct)

        print("\nFull Mask: retrievable with the .correct_mask attribute")
        print(mask_with_margins)

        print(self.correct_mask)

    def cluster_wrong_answers(self):
        """
        Find out if wrong answers have anything in common.

        :return:
        """
        pass

    def find_most_variance(self):
        """
        This function finds the samples that had
        the most variance across them.

        Highest std / variance.

        What does this mean in terms of Classification?
        Most different guesses.


        :return:
        """
        pass

    def analyze_ensemble(self):
        pass

    def add_to_ensembled_preds_df_with_ensemble_func(self):
        """
        Generalize the below to deal with any aggregation function.

        :return:
        """

    def add_metric_to_metric_df(self,
                                func,
                                func_name):
        """
        I've been concatenating but this leaves double rows
        of the same metric.

        Solve this problem by calling this function when adding
        another metric to a DF that already has other metrics
        OR is blank.

        :return:
        """
        new_preds = func(axis=1)

        # TODO: Check for Rounding Bias
        new_preds_df = pd.DataFrame(new_preds, columns=[func_name]).round(decimals = 0).astype(int)

        # ADD: IF THERE IS ALREADY A MEAN ROW, DROP IT.
        # Code here

        # Add Here
        self.ensembled_preds_df = pd.concat([self.ensembled_preds_df, new_preds_df], axis = 1)


    def fit_mean_ensemble(self):
        self.add_metric_to_metric_df(self.preds_df.mean,
                                     "mean_ensemble")


    def fit_median_ensemble(self):
        self.add_metric_to_metric_df(self.preds_df.median,
                                     "median_ensemble")

    def fit_mode_ensemble(self):

        # This doesn't work.
        # Gives ValueError: Cannot convert non-finite values (NA or inf) to integer

        #self.add_metric_to_metric_df(self.preds_df.mode,
        #                             "mode_ensemble")
        pass

    def fit_all_stats_ensembles(self):

        self.fit_mean_ensemble()
        self.fit_median_ensemble()


    def fit_best_ensemble(self):
        """

        :return:
        """
        pass

    def fit_null_test(self):
        """
        Create random predictions in a certain range
        and see how that compares with your other
        models.

        :return:
        """
        pass

    def fit_random_seed_variance(self):
        """
        How much variance is there in just changing the random seed
        :return:
        """
        pass

    def correlated_predictions(self):
        """
        Get diverse predictors by finding uncorrelated predictions.

        :return:
        """
        pass

    def ensemble_from_pred_columns(self):
        pass

    def combinatorial_ensemble(self):

        self.ensemble_comb_preds = pd.DataFrame(index = self.preds_df.index)

        cols = self.preds_df.columns
        length_cols = len(cols)

        for num_columns in range(2, length_cols):
            column_combinations = combinations(cols, num_columns)

            for the_cols in column_combinations:
                # Put ensembler loop in here.

                pass


    def bootstrap(self):
        pass

