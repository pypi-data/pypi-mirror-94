"""
An ensemble analysis.
"""

import pandas as pd
import seaborn as sns
from glob import glob

class BaseEnsembleAnalyzer:
    def __init__(self):
        self.submissions = []

    def add_csvs(self, dfs):
        for df in dfs:
            self.submissions.append(df)

    def add_csv(self, df):
        pass

    def load_from_directory(self):
        pass

    def validate_submissions(self):
        # Check if same shape

        pass

    def correlation_analysis(self):

        df_names = list(range(len(self.submissions)))
        self.corr_df = pd.DataFrame(columns = df_names,
                                    index = df_names)  # Copy a submission.

        self.correlations = []
        self.mean_correlations = []

        for i, sub in enumerate(self.submissions):
            for j, sub2 in enumerate(self.submissions):

                this_corr = sub.corrwith(sub2)
                this_corr.rename(str(i) + "_and_" + str(j))

                # self.correlations.append(this_corr)

                mean_corr = round(this_corr.mean(), 2)
                self.mean_correlations.append(mean_corr)
                self.corr_df.iloc[i,j] = mean_corr


class RegressionEnsembleAnalyzer(BaseEnsembleAnalyzer):
    def __init__(self):
        self.submissions = []

    def most_similar_predictions(self):
        pass

    def most_different_predictions(self):
        pass

    def analyze(self):
        pass

class MultiOutRegressionEnsembleAnalyzer(BaseEnsembleAnalyzer):
    def __init__(self):
        self.submissions = []


