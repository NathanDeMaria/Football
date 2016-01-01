import os
import pandas as pd


def load_data():
    """
    Read in the play by play data
    :return: DataFrame of play by play data
    """
    this_dir = os.path.dirname(os.path.realpath(__file__))
    plays_csv = os.path.join(this_dir, '..', 'plays.csv')
    return pd.read_csv(plays_csv)
