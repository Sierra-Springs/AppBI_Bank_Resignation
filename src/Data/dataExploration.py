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


def plot_numeric_distributions(table, tableName):
    """
    Produit des graphiques de la distribution des valeurs pour chaque colonne numérique de table
    :param table: pandas dataframe
    :param tableName: nom de la table
    """
    plotPath = f"{figPath}/numeric_distribution/{tableName}"
    os.makedirs(plotPath, exist_ok=True)

    table_num = table.select_dtypes(include=[np.number])

    for col in table_num.columns:
        plt.title(f"{col} distribution in {tableName}")
        sns.distplot(table_num[col], hist=False, kde=True,
                     kde_kws={'linewidth': 3})
        plt.savefig(f"{plotPath}/{col}.png")
        plt.show()


def is_equal_to(df, value):
    """
    retourne le resultat de la comparaison ligne par ligne entre une colonne de dataframe et une valeur.
    Si la valeur à comparer est None, utilisation de la méthode isnull()
    :param df:
    :param value:
    :return:
    """
    if value is None:
        return df.isnull()
    else:
        return df == value


def explore_table_missing_values(table, cols, null_vals):
    """
    Retourne un dictionnaire contenant des informations sur le nombre de données manquantes pour les colones cols
    indiquées et les valeurs nulles null_vals indiquée par colonne
    :param table:
    :param cols:
    :param null_vals:
    :return:
    """
    nb_lines = len(table)

    res = {"nb_lines": nb_lines,
           "cols": dict()
           }

    for col, null_val in zip(cols, null_vals):
        table_col = table[col]
        nb_null = sum(is_equal_to(table_col, null_val))
        percent_null = nb_null * 100 / nb_lines
        print(f"col:{col}, null:{null_val}. {nb_null}/{nb_lines} : {percent_null:.3f}%")
        res["cols"][col] = {"null_value": null_val,
                            "nb_null": nb_null,
                            "percent_null": percent_null}

    return res


def compute_df_covariance(table, tableName):
    nb_col_by_line = 6
    with open(f"{textPartsPath}/tables/{tableName}_corr.tex", 'w') as outfile:
        corr = table.corr()
        cols = corr.columns.values
        sep_cols = [[cols[j * nb_col_by_line + i] for i in range(nb_col_by_line)] for j in
                    range(len(cols) // nb_col_by_line)]
        sep_cols.append(cols[-1 * (len(cols) % nb_col_by_line):].tolist())

        for current_cols in sep_cols:
            corr.to_latex(buf=outfile,
                          float_format="%.2f",
                          columns=current_cols,
                          col_space=2)
            outfile.write("\n")



if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    table1 = pd.read_csv("Data/donnees_banque/table1.csv")
    table2 = pd.read_csv("Data/donnees_banque/table2.csv")

    blueprint("table 1")
    compute_df_covariance(table=table1, tableName="table1")
    compute_df_covariance(table=table2, tableName="table2")

    pprint(explore_table_missing_values(table=table1,
                                        cols=[CN_MTREV, CCN_RANGADH],
                                        null_vals=[V_MTREV_NULL, V_RANGADH_NULL]))

    plot_numeric_distributions(table=table1,
                               tableName="table1")

    print()
    blueprint("table 2")
    pprint(explore_table_missing_values(table=table2,
                                        cols=[CS_DTNAIS, CN_MTREV],
                                        null_vals=[V_DTNAIS_NULL, V_MTREV_NULL]))

    plot_numeric_distributions(table=table2,
                               tableName="table2")

