import patsy
import numpy as np
from statsmodels.api import load


def predict(data, formula, model_file):
    """
    Get the probability for all rows
    :param data: DataFrame of the data
    :param formula: formula used in the predictor
    :param model_file: *.pickle file containing the model
    :return: np.array of probabilities
    """
    model = load(model_file)
    _, transformed_data = patsy.dmatrices(formula, data, return_type='dataframe')
    log_odds = (transformed_data * model.params).sum(axis=1)
    return np.exp(log_odds) / (1 + np.exp(log_odds))
