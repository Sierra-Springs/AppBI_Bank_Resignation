from sklearn.preprocessing import OneHotEncoder, StandardScaler
from Utils.names import *


class DataTransformer:
    def __init__(self):
        self.fit_on = None
        self.preprocesseur = None

    def return_custom(self, data):
        return data

    def transform(self, data, data_type):
        if self.fit_on == "all" or data_type == self.fit_on:
            self.preprocesseur.fit(data.array.reshape(-1, 1))
        data_transformed = self.preprocesseur.transform(data.array.reshape(-1, 1))
        return self.return_custom(data_transformed)


class StandardScalerTransformer(DataTransformer):
    def __init__(self):
        self.fit_on = "all"
        self.preprocesseur = StandardScaler()


class OneHotEncoderTransformer(DataTransformer):
    def __init__(self):
        self.fit_on = TRAIN
        self.preprocesseur = OneHotEncoder()

    def return_custom(self, data):
        return data.toarray()


class OrdinalEncoderTransformer(DataTransformer):
    def __init__(self):
        self.fit_on = TRAIN
        self.preprocesseur = OneHotEncoder()

    def return_custom(self, data):
        return data.toarray()
