import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Utils.pathsDefinition import *
from Utils.names import *


def plot_numeric_distributions():
    table1 = pd.read_csv("Data/donnees_banque/table1.csv")

    print(table1.describe())
    print(table1.columns)
    table1_num = table1.select_dtypes(include=[np.number])

    print(table1_num.columns)
    for col in table1_num.columns:
        # plt.hist(table1[col])
        plt.title(col)
        sns.distplot(table1_num[col], hist=False, kde=True,
                     kde_kws={'linewidth': 3})
        plt.savefig(f"{figPath}/{col}.png")
        plt.show()


def plot_non_numeric_distributions():
    table1 = pd.read_csv("Data/donnees_banque/table2.csv")

    print(len(table1["DTNAIS"][table1["DTNAIS"] == V_DATE_NULL]))
    print(len(table1))

if __name__ == "__main__":
    #plot_numeric_distributions()
    #plot_non_numeric_distributions()
    table1 = pd.read_csv("Data/donnees_banque/table1.csv")

    print(table1.describe())
    print(table1.columns)

