# Ordre des opérations :
# - Suppr indivividus avec "0000-00-00" et "1900-01-00"
# - Calcul durée ADH tab2
# - Calcul age adhésion tab2
# - Ajout attribut ISDEM -> label
# - Concat tables sur les attributs nécessaires à l'analyse


import pandas as pd

from Utils.names import *


def eliminate_odd_subjects_tab2(tab):
    idx_to_remove = []
    for line in tab.index:
        if tab.loc[line][CS_DTNAIS] == V_DATE_NULL or tab.loc[line][CS_DTNAIS] == V_DATE_ODD:
            idx_to_remove.append(line)

    new_tab = tab.drop(idx_to_remove)
    new_tab.reset_index()
    return new_tab


def parse_year_dem(date):
    value = int(date.split("/")[2])
    if value == 1900:  # Si non démissionnaire
        value = 2007
    return value


def add_adh_tab2(tab):
    year_adh = tab[CS_DTADH].apply(lambda serie: int(serie.split("/")[2]))
    year_dem = tab[CS_DTDEM].apply(lambda serie: parse_year_dem(serie))
    tab[CN_ADH] = year_dem - year_adh


def add_agead_tab2(tab):
    year_adh = tab[CS_DTADH].apply(lambda serie: int(serie.split("/")[2]))
    year_nais = tab[CS_DTNAIS].apply(lambda serie: int(serie.split("/")[2]))
    tab[CN_AGEAD] = year_adh - year_nais


def add_isdem(tab1, tab2):
    tab1[CCN_ISDEM] = 1
    tab2[CCN_ISDEM] = tab2[CS_DTDEM].apply(lambda value: 0 if value == V_DTDEM_NO_DEM else 1)


def concat_tables(tab1, tab2):
    columns = [CCN_CDSEXE, CN_MTREV, CN_NBENF, CCN_CDSITFAM, CCN_CDTMT, CCN_CDCATCL, CN_AGEAD, CN_ADH, CCN_ISDEM]
    new_tab1 = tab1[columns]
    new_tab2 = tab2[columns]
    final_table = pd.concat([new_tab1, new_tab2], ignore_index=True)
    return final_table


def data_prepare():
    tab1 = pd.read_csv("Data/donnees_banque/table1.csv")
    tab2 = pd.read_csv("Data/donnees_banque/table2.csv")

    tab2 = eliminate_odd_subjects_tab2(tab2)
    add_adh_tab2(tab2)
    add_agead_tab2(tab2)
    add_isdem(tab1, tab2)

    concat_table = concat_tables(tab1, tab2)

    return concat_table


if __name__ == "__main__":
    # pd.set_option('display.max_rows', None)

    table1 = pd.read_csv("Data/donnees_banque/table1.csv")
    table2 = pd.read_csv("Data/donnees_banque/table2.csv")

    print(table2.shape)
    table2 = eliminate_odd_subjects_tab2(table2)
    print(table2.shape)
    add_adh_tab2(table2)
    print(table2.shape)
    add_agead_tab2(table2)
    print(table2.shape)
    add_isdem(table1, table2)
    print(table2.shape)

    print(table2.head())
    print(table2)

    concat_tables(table1, table2)
