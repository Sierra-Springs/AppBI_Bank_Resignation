import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler


from Data.dataPreparation import *

from Utils.pathsDefinition import *
from Utils.names import *
from Utils.ColorPrinter import *


class DataProvider:
    def __init__(self):
        self.table = data_prepare()
        self.splitted_data = dict()
        self.data = dict()

    def get_data_prepare(self, train_percent, valid_percent, test_percent,
                         numeric_preparator=StandardScaler(), categorical_preparator=OneHotEncoder()):
        if not self.splitted_data:
            self.get_splitted_data(train_percent, valid_percent, test_percent)
        pd.set_option('display.max_columns', None)
        for data_type in [TRAIN, VALID, TEST]:
            # traitement des données catégorielles
            cat = self.splitted_data[data_type][LIST_KEPT_CAT_COLS]
            if data_type == TRAIN:
                categorical_preparator.fit(cat)

            cat_transformed = categorical_preparator.transform(cat).toarray()
            cat_transformed = pd.DataFrame(cat_transformed, index=cat.index, columns=[i for i in range(cat_transformed.shape[1])])

            # traitement des données numériques
            num = self.splitted_data[data_type][LIST_KEPT_NUM_COLS]
            num_transformed = numeric_preparator.fit_transform(num)
            num_transformed = pd.DataFrame(num_transformed, index=num.index, columns=num.columns)
            self.data[data_type] = dict()
            self.data[data_type]["X"] = pd.concat([cat_transformed, num_transformed], axis=1)
            self.data[data_type]["Y"] = self.splitted_data[data_type][CCN_ISDEM]


        return self.data


    def get_splitted_data(self, train_percent, valid_percent, test_percent):
        assert train_percent + valid_percent + test_percent == 1, "La somme des pourcentage doit être égale à 1"
        test_percent = 1 - (train_percent + valid_percent)
        blueprint(f"Splitting data into train ({train_percent}), valid ({valid_percent}), test ({test_percent})")

        dem = self.table[self.table[CCN_ISDEM] == 1]
        dem = dem.sample(frac=1, random_state=0).reset_index(drop=True)

        end_train = int(train_percent * dem.shape[0])
        end_valid = int((train_percent + valid_percent) * dem.shape[0])
        dem_train = dem[:end_train]
        dem_valid = dem[end_train:end_valid]
        dem_test = dem[end_valid:]

        not_dem = self.table[self.table[CCN_ISDEM] == 0]
        not_dem = not_dem.sample(frac=1, random_state=0).reset_index(drop=True)

        end_train = int(train_percent * not_dem.shape[0])
        end_valid = int((train_percent + valid_percent) * not_dem.shape[0])
        not_dem_train = not_dem[:end_train]
        not_dem_valid = not_dem[end_train:end_valid]
        not_dem_test = not_dem[end_valid:]

        self.splitted_data[TRAIN] = pd.concat([dem_train, not_dem_train], ignore_index=True)
        self.splitted_data[VALID] = pd.concat([dem_valid, not_dem_valid], ignore_index=True)
        self.splitted_data[TEST] = pd.concat([dem_test, not_dem_test], ignore_index=True)

        self.splitted_data[TRAIN] = self.splitted_data[TRAIN].sample(frac=1, random_state=0).reset_index(drop=True)
        self.splitted_data[VALID] = self.splitted_data[VALID].sample(frac=1, random_state=0).reset_index(drop=True)
        self.splitted_data[TEST] = self.splitted_data[TEST].sample(frac=1, random_state=0).reset_index(drop=True)

        return self.splitted_data


if __name__ == "__main__":
    print(table1Path)
    dataProvider = DataProvider()
    data = dataProvider.get_splitted_data(.30, .30)

    for key in data.keys():
        blueprint(key)
        print(data[key])
        print()