"""

Author: Thomas Meli
Purpose: To help discern which models do best and worst on different samples.

"""


import pandas as pd
import numpy as np
import seaborn as sns

class Analyzer:
    """
    The main object of
    """

    def __init__(self,
                 df: pd.DataFrame,
                 y_true: str = "y_true"):
        """

        :param df: pd.Dataframe - Dataframe with predictions and y_true column.
        :param y_true:
        """

        # self.y_true = df.pop("y_true)
        #
        # self.preds = preds
        # self.df = df

        pass

    def _validate_df(self):
        pass

    def fit(self):
        """

        """
        pass

    def get_statistics(self):
        """

        """

        # self.statistics = None.
        # return self.statistics

        pass

    def get_metrics(self):
        """

        :return:
        """

        pass

