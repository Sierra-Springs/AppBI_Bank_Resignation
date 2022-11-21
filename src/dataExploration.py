import pandas as pd


if __name__ == "__main__":
    table1 = pd.read_csv("Data/donnees_banque/table1.csv")

    print(table1.describe())