import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler


from Data.dataPreparation import *
from Data.DataTransformer import *

from Utils.pathsDefinition import *
from Utils.names import *
from Utils.ColorPrinter import *


class DataProvider:
    splitted_data = dict()
    table = data_prepare()
    train_percent = .60
    valid_percent = .20
    test_percent = .20

    def __init__(self, transformers):
        self.transformers = transformers
        self.data = dict()

    @classmethod
    def set_percents(cls, train_percent, valid_percent, test_percent):
        cls.train_percent = train_percent
        cls.valid_percent = valid_percent
        cls.test_percent = test_percent

    @classmethod
    def get_splitted_data(cls):
        assert cls.train_percent + cls.valid_percent + cls.test_percent == 1, "La somme des pourcentage doit être égale à 1"
        blueprint(f"Splitting data into train ({cls.train_percent}), valid ({cls.valid_percent}), test ({cls.test_percent})")

        dem = cls.table[cls.table[CCN_ISDEM] == 1]
        dem = dem.sample(frac=1, random_state=0).reset_index(drop=True)

        end_train = int(cls.train_percent * dem.shape[0])
        end_valid = int((cls.train_percent + cls.valid_percent) * dem.shape[0])
        dem_train = dem[:end_train]
        dem_valid = dem[end_train:end_valid]
        dem_test = dem[end_valid:]

        not_dem = cls.table[cls.table[CCN_ISDEM] == 0]
        not_dem = not_dem.sample(frac=1, random_state=0).reset_index(drop=True)

        end_train = int(cls.train_percent * not_dem.shape[0])
        end_valid = int((cls.train_percent + cls.valid_percent) * not_dem.shape[0])
        not_dem_train = not_dem[:end_train]
        not_dem_valid = not_dem[end_train:end_valid]
        not_dem_test = not_dem[end_valid:]

        cls.splitted_data[TRAIN] = pd.concat([dem_train, not_dem_train], ignore_index=True)
        cls.splitted_data[VALID] = pd.concat([dem_valid, not_dem_valid], ignore_index=True)
        cls.splitted_data[TEST] = pd.concat([dem_test, not_dem_test], ignore_index=True)

        cls.splitted_data[TRAIN] = cls.splitted_data[TRAIN].sample(frac=1, random_state=0).reset_index(drop=True)
        cls.splitted_data[VALID] = cls.splitted_data[VALID].sample(frac=1, random_state=0).reset_index(drop=True)
        cls.splitted_data[TEST] = cls.splitted_data[TEST].sample(frac=1, random_state=0).reset_index(drop=True)

        return cls.splitted_data

    def get_data_prepare(self):
        if not DataProvider.splitted_data:
            DataProvider.get_splitted_data()

        for data_type in [TRAIN, VALID, TEST]:
            col_transformed = []
            for col in self.transformers.keys():
                col_df = DataProvider.splitted_data[data_type][col]
                col_transformed.append(self.transformers[col].transform(col_df, data_type))
                col_transformed[-1] = pd.DataFrame(col_transformed[-1],
                                                   index=col_df.index,
                                                   columns=[i for i in range(col_transformed[-1].shape[1])])

            self.data[data_type] = dict()
            self.data[data_type]["X"] = pd.concat(col_transformed, axis=1)
            self.data[data_type]["Y"] = DataProvider.splitted_data[data_type][CCN_ISDEM]

        return self.data


class SVMDataProvider(DataProvider):
    def __init__(self):
        transformers = dict()
        for col_name in LIST_KEPT_CAT_COLS:
            transformers[col_name] = OneHotEncoderTransformer()
        for col_name in LIST_KEPT_NUM_COLS:
            transformers[col_name] = StandardScalerTransformer()
        super().__init__(transformers)


class NaiveBayesDataProvider(DataProvider):
    def __init__(self):
        transformers = dict()
        for col_name in LIST_KEPT_CAT_COLS:
            transformers[col_name] = OneHotEncoderTransformer()
        for col_name in LIST_KEPT_NUM_COLS:
            transformers[col_name] = StandardScalerTransformer()
        super().__init__(transformers)
