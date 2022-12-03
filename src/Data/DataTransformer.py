from sklearn.preprocessing import OneHotEncoder, StandardScaler, KBinsDiscretizer
import pandas as pd
from Utils.names import *


class DataTransformer:
    def __init__(self, fit_on, preprocessor):
        self.fit_on = fit_on
        self.preprocessor = preprocessor

    def inprocessing(self, data):
        return data

    def transform(self, data, col_prefix_name, data_type):
        if self.fit_on == "all" or data_type == self.fit_on:
            self.preprocessor.fit(data.array.reshape(-1, 1))
        data_transformed = self.preprocessor.transform(data.array.reshape(-1, 1))
        data_transformed = self.inprocessing(data_transformed)
        columns = [f"{col_prefix_name}_{i}" for i in range(data_transformed.shape[1])]
        data_transformed = pd.DataFrame(data_transformed, index=data.index, columns=columns)

        return data_transformed


class DoNothingTransformer(DataTransformer):
    def transform(self, data, col_prefix_name, data_type):
        return data


class StandardScalerTransformer(DataTransformer):
    def __init__(self):
        fit_on = "all"
        preprocesseur = StandardScaler()
        super().__init__(fit_on=fit_on, preprocessor=preprocesseur)


class OneHotEncoderTransformer(DataTransformer):
    def __init__(self):
        fit_on = TRAIN
        preprocesseur = OneHotEncoder()
        super().__init__(fit_on=fit_on, preprocessor=preprocesseur)

    def inprocessing(self, data):
        return data.toarray()


class KBinsDiscretizerTransformer(DataTransformer):
    def __init__(self, n_bins, encode, strategy):
        fit_on = TRAIN
        preprocessor = KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy)
        super().__init__(fit_on=fit_on, preprocessor=preprocessor)


class OrdinalEncoderTransformer(DataTransformer):
    def __init__(self):
        fit_on = TRAIN
        preprocessor = OneHotEncoder()
        super().__init__(fit_on=fit_on, preprocessor=preprocessor)

    def inprocessing(self, data):
        return data.toarray()


if __name__ == '__main__':
    from Data.dataPreparation import *
    table = data_prepare()
    ntct = KBinsDiscretizerTransformer(n_bins=10, encode='ordinal', strategy="uniform")
    print(ntct.transform(table[CN_AGEAD], CN_AGEAD, "TRAIN"))
