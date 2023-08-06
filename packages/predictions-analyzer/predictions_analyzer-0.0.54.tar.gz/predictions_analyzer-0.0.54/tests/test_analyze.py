"""
Unit tests for analyze.py
"""

from predictions_analyzer.analyze import *

def _validate_df():
    pass

def test_constructor():

    df = pd.DataFrame()
    assert Analyzer(df)