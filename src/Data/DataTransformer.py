from sklearn.preprocessing import OneHotEncoder, StandardScaler
from Utils.names import *


class DataTransformer:
    def __init__(self, fit_on, preprocesseur):
        self.fit_on = fit_on
        self.preprocesseur = preprocesseur

    def return_custom(self, data):
        return data

    def transform(self, data, data_type):
        if self.fit_on == "all" or data_type == self.fit_on:
            self.preprocesseur.fit(data.array.reshape(-1, 1))
        data_transformed = self.preprocesseur.transform(data.array.reshape(-1, 1))
        return self.return_custom(data_transformed)


class DoNothingTransformer(DataTransformer):
    class DoNothingPreprocesseur:
        def fit(self, _):
            pass

        def transform(self, data):
            return data

    def __init__(self):
        fit_on = None
        preprocesseur = DoNothingTransformer.DoNothingPreprocesseur()
        super().__init__(fit_on=fit_on, preprocesseur=preprocesseur)


class StandardScalerTransformer(DataTransformer):
    def __init__(self):
        fit_on = "all"
        preprocesseur = StandardScaler()
        super().__init__(fit_on=fit_on, preprocesseur=preprocesseur)


class OneHotEncoderTransformer(DataTransformer):
    def __init__(self):
        fit_on = TRAIN
        preprocesseur = OneHotEncoder()
        super().__init__(fit_on=fit_on, preprocesseur=preprocesseur)

    def return_custom(self, data):
        return data.toarray()

