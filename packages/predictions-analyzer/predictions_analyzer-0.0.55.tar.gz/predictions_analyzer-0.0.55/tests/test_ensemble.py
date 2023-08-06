from predictions_analyzer.ensemble import *
import pandas as pd
from glob import glob

submission_path = "./test_submissions/jane/"


def get_ens():
    ens = MultiOutRegressionEnsembleAnalyzer()

    submission1 = pd.read_csv(submission_path + "submission0.csv")
    submission2 = pd.read_csv(submission_path + "submission1.csv")
    submission3 = pd.read_csv(submission_path + "submission2.csv")
    submission4 = pd.read_csv(submission_path + "submission3.csv")
    submission5 = pd.read_csv(submission_path + "submission4.csv")
    submission6 = pd.read_csv(submission_path + "submission5.csv")
#    submission7 = pd.read_csv(submission_path + "submission6.csv")
#    submission8 = pd.read_csv(submission_path + "submission7.csv")

    list_of_csvs = [submission1, submission2, submission3,
                    submission4, submission5, submission6,
 #                   submission7, submission8, submission9
                    ]

    ens.add_csvs(list_of_csvs)

    return ens

def test_multioutput_ensemble():
    ens = MultiOutRegressionEnsembleAnalyzer()

def test_add_csvs():
    ens = get_ens()

    submission1 = pd.read_csv(submission_path + "submission0.csv")
    submission2 = pd.read_csv(submission_path + "submission1.csv")
    submission3 = pd.read_csv(submission_path + "submission2.csv")

    list_of_csvs = [submission1, submission2, submission3]

    ens.add_csvs(list_of_csvs)

    print(ens.submissions)


def test_corr():
    ens = get_ens()
    ens.correlation_analysis()
    # print(ens.mean_correlations)
    print("\n", ens.corr_df)
    print("\n", ens.corr_df.mean())




