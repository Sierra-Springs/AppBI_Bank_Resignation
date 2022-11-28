import pandas as pd

from Utils.names import *


# print(table1.head())
# print(table2.head())

def eliminate_odd_subjects(table2):
    idx_to_remove = []
    # for line in range(len(table2)):
    print(table2.index)
    for line in table2.index:
        if table2.loc[line][CS_DTNAIS] == V_DATE_NULL or table2.loc[line][CS_DTNAIS] == V_DATE_ODD:
            idx_to_remove.append(line)

    new_table2 = table2.drop(idx_to_remove)
    new_table2.reset_index()
    print(new_table2.index)
    return new_table2

def parse_year_dem(date):
    value = int(date.split("/")[2])
    if value == 1900:  # Si non démissionnaire
        value = 2007
    return value


def add_adh_tab2(table2):
    year_adh = table2[CS_DTADH].apply(lambda serie: int(serie.split("/")[2]))
    year_dem = table2[CS_DTDEM].apply(lambda serie: parse_year_dem(serie))

    table2[CN_ADH] = year_dem - year_adh




def add_agead_tab2():
    year_adh = table2[CS_DTADH].apply(lambda serie: int(serie.split("/")[2]))
    year_nais = table2[CS_DTNAIS].apply(lambda serie: int(serie.split("/")[2]))

    table2[CN_AGEAD] = year_adh - year_nais

    print("==============================================")
    print(table2[[CS_DTNAIS, CS_DTADH, CS_DTDEM, CN_AGEAD, CN_ADH]])
    print("==============================================")


def add_isdem():
    table1[CCN_ISDEM] = 1
    table2[CCN_ISDEM] = table2[CS_DTDEM].apply(lambda value : 0 if value == V_DTDEM_NO_DEM else 1)



def concat_tables(table1, table2):
    print("==========================")
    columns = [CCN_CDSEXE, CN_MTREV, CN_NBENF, CCN_CDSITFAM, CCN_CDTMT, CCN_CDCATCL, CN_AGEAD, CN_ADH, CCN_ISDEM]
    new_table1 = table1[columns]
    print(new_table1)
    new_table2 = table2[columns]
    print(new_table2)
    final_table = pd.concat([new_table1, new_table2], ignore_index=True)
    print(final_table.shape)
    print(final_table)
    return final_table


def data_prepare():
    table1 = pd.read_csv("Data/donnees_banque/table1.csv")
    table2 = pd.read_csv("Data/donnees_banque/table2.csv")

    table2 = eliminate_odd_subjects(table2)
    add_adh_tab2(table2)
    add_agead_tab2(table2)
    add_isdem(table1, table2)

    concat_tables(table1, table2)


if __name__ == "__main__":
    # pd.set_option('display.max_rows', None)

    table1 = pd.read_csv("Data/donnees_banque/table1.csv")
    table2 = pd.read_csv("Data/donnees_banque/table2.csv")

    print(table2.shape)
    table2 = eliminate_odd_subjects(table2)
    print(table2.shape)
    add_adh_tab2(table2)
    print(table2.shape)
    add_agead_tab2()
    print(table2.shape)
    add_isdem()
    print(table2.shape)

    print(table2.head())
    print(table2)

    concat_tables(table1, table2)

    ## Ordre des opérations
    # - Suppr indivividus avec "0000-00-00"
    # - Calcul durée ADH tab2
    # - Calcul age adhésion tab2
    # - Concat tables sur les attributs communs