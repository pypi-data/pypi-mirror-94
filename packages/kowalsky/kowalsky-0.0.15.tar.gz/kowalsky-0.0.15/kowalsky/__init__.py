import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from .kaggle import make_sub


def analysis(model, y_column, path=None, path_test=None, path_out=None,
             ds=None, ds_test=None, export_test_set=False, sample_path=None,
             rounds=1, eval_model=True, target_transform_fn=None):
    if ds is None:
        ds = pd.read_csv(path)

    X, y = ds.drop(y_column, axis=1), ds[y_column]

    if eval_model:
        print(np.array(
            [cross_val_score(model, X, y, n_jobs=-1).mean() for _ in range(rounds)]
        ).mean())

    if export_test_set and \
            path_out is not None and \
            sample_path is not None and \
            (path_test is not None or ds_test is not None):
        if ds_test is None:
            ds_test = pd.read_csv(path_test)
        model.fit(X, y)

        preds = model.predict(ds_test)

        if target_transform_fn is not None:
            preds = target_transform_fn(preds)
        make_sub(preds, path_out, sample_path, y_column)
