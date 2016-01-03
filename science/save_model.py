from load_data import load_data
from statsmodels.formula.api import logit


FORMULA = 'offense_win ~ time_left : score_diff + score_diff + C(down) + distance + field_position'
MODEL_FILE = '../model.pickle'


def fit_model(formula, model_file):
    """
    Saves a model
    :param formula: formula for the model
    :param model_file: name of file to save the model to
    """
    data = load_data()
    model = logit(formula=formula, data=data)
    fitted = model.fit()
    fitted.save(model_file)


if __name__ == '__main__':
    fit_model(FORMULA, MODEL_FILE)
