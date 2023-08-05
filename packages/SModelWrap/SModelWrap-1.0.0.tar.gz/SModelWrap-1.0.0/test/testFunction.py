from unittest import TestCase
from numpy import ndarray
from pandas import DataFrame, Timestamp
from SModelWrap import ModelPerClass


class FakeModel():
    """
    Fakemodel: Just returns the first val
    """

    def predict(self, x_val: DataFrame) -> ndarray:
        column = x_val.columns.tolist()[0]
        return x_val[column].to_numpy()


class TestThings(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        data = ["5", "4", "3", "3", "2", "2", "1", "1"]
        index = [
            Timestamp('20130101 09:00:02'),
            Timestamp('20130101 09:00:02'),
            Timestamp('20130101 09:00:03'),
            Timestamp('20130101 09:00:05'),
            Timestamp('20130101 09:00:08'),
            Timestamp('20130101 09:00:08'),
            Timestamp('20130101 09:00:09'),
            Timestamp('20130101 09:00:09'),
        ]
        cls.model_dict = {K: FakeModel() for K in set(data)}

        cls.fakedata = DataFrame({"data": data, "d2": data[::-1]}, index=index)

    def test_predict(self):
        model = ModelPerClass(model_dict=self.model_dict, column_key='data')
        predictions = model.predict(self.fakedata)
        print(predictions)
        self.assertEqual(self.fakedata['data'].tolist(), [x[0] for x in predictions.tolist()])
