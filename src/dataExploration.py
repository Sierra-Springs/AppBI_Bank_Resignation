import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    table1 = pd.read_csv("Data/donnees_banque/table1.csv")

    print(table1.describe())
    print(table1.columns)
    table1_num = table1.select_dtypes(include=[np.number])

    print(table1_num.columns)
    for col in table1_num.columns:
        #plt.hist(table1[col])
        plt.title(col)
        sns.distplot(table1_num[col], hist=False, kde=True,
                     kde_kws={'linewidth': 3})
        plt.show()

