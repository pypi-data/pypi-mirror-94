from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_squared_error


def rmsle(actual, pred):
    pred[pred < 0] = 0
    return mean_squared_log_error(actual, pred) ** 0.5


def rmse(actual, pred):
    return mean_squared_error(actual, pred) ** 0.5
