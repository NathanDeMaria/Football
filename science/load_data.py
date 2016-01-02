import os
import pandas as pd


def raw_data():
    """
    Read in the play by play data
    :return: DataFrame of play by play data
    """
    this_dir = os.path.dirname(os.path.realpath(__file__))
    plays_csv = os.path.join(this_dir, '..', 'plays.csv')
    return pd.read_csv(plays_csv)


def load_data():
    """
    Loads the data with some computed features
    :return: DataFrame of play data
    """
    data = raw_data()
    data['offense_win'] = (data.offense_final > data.defense_final).astype(int)
    data['score_diff'] = data.offense_score - data.defense_score
    data['score_rate'] = data.score_diff / data.time_left
    return data
