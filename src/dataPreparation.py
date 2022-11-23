import pandas as pd

from Utils.names import *


# print(table1.head())
# print(table2.head())

def eliminate_odd_subjects():
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

def compute_age(ya, yd):
    # print(ya, yd)
    year_adh = ya.apply(lambda serie : int(serie.split("/")[2]))
    print(year_adh)
    year_dem = yd.apply(lambda serie : (x if x:=int(serie.split("/")[2] == 200)))
    print(year_dem)
    if year_dem == 1900:  # Si non démissionnaire
        year_dem = 2007
    input()
    return year_dem - year_adh


def add_adh_tab2():
    sub_tab2 = table2[[CS_DTADH, CS_DTDEM]]
    durations = []
    # for line in range(len(sub_tab2)):
    # for line in table2.index:
    #     dates = sub_tab2.loc[line].values.tolist()
    #     year_adh = int(dates[0].split("/")[2])
    #     year_dem = int(dates[1].split("/")[2])
    #     if year_dem == 1900:  # Si non démissionnaire
    #         year_dem = 2007
    #     durations.append(year_dem - year_adh)
    # adh_tab2 = pd.Series(durations)
    # table2[CN_ADH] = adh_tab2
    table2[CN_ADH] = table2.apply(lambda row : compute_age(table2[CS_DTADH], table2[CS_DTDEM]), axis=1)




def add_agead_tab2():
    sub_tab2 = table2[[CS_DTADH, CS_DTNAIS]]
    durations = []
    # for line in range(len(sub_tab2)):
    for line in table2.index:
        dates = sub_tab2.loc[line].values.tolist()
        # print(dates)
        year_adh = int(dates[0].split("/")[2])
        year_nais = int(dates[1].split("/")[2])
        durations.append(year_adh - year_nais)
    nais_tab2 = pd.Series(durations)
    table2[CN_AGEAD] = nais_tab2
    print("==============================================")
    print(table2[[CS_DTNAIS, CS_DTADH, CS_DTDEM, CN_AGEAD, CN_ADH]])
    print("==============================================")


def add_isdem():
    # table1
    isdem1 = []
    for line in table1.index:
        isdem1.append(1)
    isdem_tab1 = pd.Series(isdem1)
    table1[CCN_ISDEM] = isdem_tab1

    #table2
    sub_tab2 = table2[[CS_DTDEM]]
    isdem2 = []
    # for line in range(len(sub_tab2)):
    for line in table2.index:
        date_dem = sub_tab2.loc[line].values.tolist()
        year_dem = int(date_dem[0].split("/")[2])
        if year_dem == 1900:  # Si non démissionnaire
            isdem2.append(0)
        else:
            isdem2.append(1)
    isdem_tab2 = pd.Series(isdem2)
    table2[CCN_ISDEM] = isdem_tab2


def concat_tables():
    print("==========================")
    columns = [CCN_CDSEXE, CN_MTREV, CN_NBENF, CCN_CDSITFAM, CCN_CDTMT, CCN_CDCATCL, CN_AGEAD, CN_ADH, CCN_ISDEM]
    new_table1 = table1[columns]
    print(new_table1)
    new_table2 = table2[columns]
    print(new_table2)
    final_table = pd.concat([new_table1, new_table2], ignore_index=True)
    print(final_table.shape)
    print(final_table)


table1 = pd.read_csv("Data/donnees_banque/table1.csv")
table2 = pd.read_csv("Data/donnees_banque/table2.csv")

print(table2.shape)
table2 = eliminate_odd_subjects()
print(table2.shape)
add_adh_tab2()
print(table2.shape)
add_agead_tab2()
print(table2.shape)
add_isdem()
print(table2.shape)

print(table2.head())
print(table2)

concat_tables()

## Ordre des opérations
# - Suppr indivividus avec "0000-00-00"
# - Calcul durée ADH tab2
# - Calcul age adhésion tab2
# - Concat tables sur les attributs communs