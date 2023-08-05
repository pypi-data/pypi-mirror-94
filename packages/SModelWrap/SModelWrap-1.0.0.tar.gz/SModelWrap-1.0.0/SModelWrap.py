from pandas import DataFrame
from numpy import ndarray
import pandas as pd


class ModelPerClass:
    """
    Wrapper around a generic Model (SciKitLearn or otherwise).
    Goal is for you to provide a dict of trained models and the relevent key,
    Does not implement predict_proba (because array sizes are going to be different sizes so this won't work with
    stacking.
    """

    def __init__(self, model_dict: dict, column_key: str):
        """

        :param model_dict:
        :type model_dict: Any trained model that has a predict method
        :param column_key: key of the column to get this key from
        :type column_key: str
        """
        self.model_dict = model_dict
        self.column_key = column_key
        self._data = DataFrame

    def predict(self, x_val: DataFrame) -> ndarray:
        """

        :param x_val: X values to be predicted
        :type x_val: Pandas DataFrame
        :return: array of predictions
        :rtype: ndarray
        """
        return_df = None
        if not isinstance(x_val, DataFrame):
            raise ValueError(f"Provided values were of type {type(x_val)}, expected DataFrame")
        x_val.reset_index(drop=True, inplace=True)
        for key, model in self.model_dict.items():
            data_to_use = x_val.loc[x_val[self.column_key] == key].drop(self.column_key, axis=1)
            indexes = data_to_use.index.tolist()
            predictions = DataFrame(index=indexes, data=model.predict(data_to_use))
            if return_df is None:
                return_df = predictions
            else:
                return_df = pd.concat([return_df, predictions])
        return return_df.sort_index(ascending=False, inplace=False).to_numpy()
