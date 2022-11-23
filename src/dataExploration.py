import warnings

warnings.filterwarnings("ignore")

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Utils.pathsDefinition import *
from Utils.names import *
from Utils.ColorPrinter import *

from pprint import pprint


def plot_numeric_distributions(tablePath, tableName):
    plotPath = f"{figPath}/numeric_distribution/{tableName}"
    os.makedirs(plotPath, exist_ok=True)
    table = pd.read_csv(tablePath)

    print(table.describe())
    print(table.columns)
    table_num = table.select_dtypes(include=[np.number])

    print(table_num.columns)
    for col in table_num.columns:
        # plt.hist(table1[col])
        plt.title(col)
        sns.distplot(table_num[col], hist=False, kde=True,
                     kde_kws={'linewidth': 3})
        plt.savefig(f"{plotPath}/{col}.png")
        plt.show()


def is_equal_to(df, value):
    if value is None:
        return df.isnull()
    else:
        return df == value


def explore_table_missing_values(tablepath, cols, null_vals):
    table1 = pd.read_csv(tablepath)
    nb_lines = len(table1)

    res = {"nb_lines": nb_lines,
           "cols": dict()
           }

    for col, null_val in zip(cols, null_vals):
        table_col = table1[col]
        nb_null = sum(is_equal_to(table_col, null_val))
        percent_null = nb_null * 100 / nb_lines
        print(f"col:{col}, null:{null_val}. {nb_null}/{nb_lines} : {percent_null:.3f}%")
        res["cols"][col] = {"null_value": null_val,
                            "nb_null": nb_null,
                            "percent_null": percent_null}

    return res


if __name__ == "__main__":
    blueprint("table 1")
    pprint(explore_table_missing_values(tablepath="Data/donnees_banque/table1.csv",
                                        cols=[CN_MTREV, CCN_RANGADH],
                                        null_vals = [V_MTREV_NULL, V_RANGADH_NULL]))

    plot_numeric_distributions(tablePath="Data/donnees_banque/table1.csv",
                               tableName="table1")

    print()
    blueprint("table 2")
    pprint(explore_table_missing_values(tablepath="Data/donnees_banque/table2.csv",
                                        cols=[CS_DTNAIS, CN_MTREV],
                                        null_vals = [V_DTNAIS_NULL, V_MTREV_NULL]))

    plot_numeric_distributions(tablePath="Data/donnees_banque/table2.csv",
                               tableName="table2")

