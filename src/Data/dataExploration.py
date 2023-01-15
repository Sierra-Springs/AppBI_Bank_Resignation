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

from dataPreparation import data_prepare


def plot_numeric_distributions(df, tableName, method="distplot"):
    """
    Produit des graphiques de la distribution des valeurs pour chaque colonne numérique de table
    :param df: pandas dataframe
    :param tableName: nom de la table
    """
    plotters = {"distplot": sns.distplot,
                "boxplot": sns.boxplot}

    plotPath = figPath / tableName / "numeric_distribution" / method
    os.makedirs(plotPath, exist_ok=True)

    if df.dtype == "category":
        ax = plotters[method](df.cat.codes)
        ax.set_xticks(range(len(df.cat.categories)), df.cat.categories)
    else:
        plotters[method](df)
    titre = f"{df.name} distribution in prepared data"
    plt.title(titre)
    plt.savefig(plotPath / f"{method}__{titre.replace(' ', '_')}.png")
    plt.show()


def export_descriptions(df):
    description = df.describe().T
    for col in df.columns:
        file_path = textPartsPath / "prepared_data" / "description" / f"{col}_description.tex"
        os.makedirs(file_path.parent, exist_ok=True)
        if df[col].dtype == "category":
            index_description = df[col].value_counts() / df[col].count()
            index_description = pd.DataFrame(index_description).T
        else:
            index_description = description[description.index == col]

        export_df_to_latex(index_description, file_path, nb_col_by_line=8)


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
    with open(textPartsPath / "tables" / f"{tableName}_corr.tex", 'w') as outfile:
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


def export_df_to_latex(df, filepath, nb_col_by_line=6, float_format="%.2f", col_space=2):
    with open(filepath, 'w') as outfile:
        cols = df.columns.values
        sep_cols = [[cols[j * nb_col_by_line + i] for i in range(nb_col_by_line)] for j in
                    range(len(cols) // nb_col_by_line)]
        sep_cols.append(cols[-1 * (len(cols) % nb_col_by_line):].tolist())

        for current_cols in sep_cols:
            df.to_latex(buf=outfile,
                        float_format=float_format,
                        columns=current_cols,
                        col_space=col_space)
            outfile.write("\n")


def raw_data_exploration():
    pd.set_option('display.max_columns', None)

    table1 = pd.read_csv(table1Path)
    table2 = pd.read_csv(table2Path)

    pprint(explore_table_missing_values(table=table1,
                                        cols=[CN_MTREV, CCN_RANGADH],
                                        null_vals=[V_MTREV_NULL, V_RANGADH_NULL]))

    plot_numeric_distributions(df=table1,
                               tableName="table1")

    print()
    blueprint("df 2")
    pprint(explore_table_missing_values(table=table2,
                                        cols=[CS_DTNAIS, CN_MTREV],
                                        null_vals=[V_DTNAIS_NULL, V_MTREV_NULL]))

    plot_numeric_distributions(df=table2,
                               tableName="table2")


def prepared_data_exploration():
    pd.set_option('display.max_columns', None)

    df = data_prepare()
    df[CCN_CDSITFAM] = pd.Categorical(df[CCN_CDSITFAM])

    blueprint("Apercu des données préparées")
    print(df)
    print()

    blueprint("Description des colones et export en Latex")
    print(df.describe())
    export_descriptions(df)
    print()

    # densités
    blueprint("Génération des graphiques de densité")
    plotPath = figPath / "prepared_data" / "numeric_distribution"
    os.makedirs(plotPath, exist_ok=True)
    for col in (*LIST_KEPT_CAT_COLS, *LIST_KEPT_NUM_COLS):
        plot_numeric_distributions(df[col], "prepared_data", "distplot")
        plot_numeric_distributions(df[col], "prepared_data", "boxplot")


if __name__ == "__main__":
    prepared_data_exploration()
