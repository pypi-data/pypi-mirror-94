
import optuna

class BaseTuner:
    def __init__(self):
        pass

    def subsample_tune(self, n = 10000):
        """
        This method is good for tuning really big datasets.

        It does an optuna experiment for each
        subsample and then reports the results
        and the statistics (confidence intervals,
        credible intervals, etc.) std dev., etc.
        associated with all of the experiments.

        :return:
        """


class FeatureTuner:
    """
    Turn feature generation into a grid search
    or bayesian optimization problem.

    """

    def __init__(self):
        pass


class ClassificationTuner:
    def __init__(self):
        pass

    def tune_add(self, remove_original = False):
        """
        Tune a model and then add it to
        a Classification Analyzer.

        remove_original

        :return:
        """

    def tune_all(self, remove_original = False):
        """
        Tune all models in a Classification
        Analyzer.

        Loops through tune_add.

        remove_original:

        :return:
        """


class RegressionTuner:
    def __init__(self):
        pass



