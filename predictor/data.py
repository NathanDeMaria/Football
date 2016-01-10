import pandas as pd

from football.pages import PlayByPlay
from model import predict


def get_data(game_id):
    """
    Get data and predictions for a game
    :param game_id: ID of game to get data for
    :return: yields dict(time_left, prediction)
    """
    pbp = PlayByPlay(game_id)
    plays = pd.DataFrame(pbp.get_play_data())
    plays = _transform_data(plays)
    predictions = predict(plays,
                          'offense_win ~ time_left : score_diff + score_diff + C(down) + distance + field_position',
                          '../model.pickle')
    predictions[plays.offense != pbp.home] = 1 - predictions[plays.offense != pbp.home]
    for time_left, prediction in zip(plays.time_left, predictions):
        yield dict(time_left=int(time_left), probability=float(prediction))


def _transform_data(data):
    """
    Add some computed features to the data
    :param data: DataFrame of play-by-play data
    NOTE: this is duplicated from science/load_data.py, might turn that into a package eventually...
    :return: DataFrame of play data
    """
    data['offense_win'] = (data.offense_final > data.defense_final).astype(int)
    data['score_diff'] = data.offense_score - data.defense_score
    data['score_rate'] = data.score_diff / data.time_left
    return data
