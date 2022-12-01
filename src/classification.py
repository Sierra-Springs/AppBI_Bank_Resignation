# SVM, KNN, Naive Bayes, +1 libre
# Découper les données en apprentissage = {train, dev}, validation, test
# Ré-équilibrer les classes (pondération des erreurs ou génération de données)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from pprint import pprint

from Data.DataProvider import *
from Models.SVM import *
from Models.NaiveBayes import *

if __name__ == '__main__':
    DataProvider.set_percents(.60, .20, .20)
    dataProvider = NaiveBayesDataProvider()

    model = NaiveBayesBase(dataProvider)
    model.train()
    metrics = model.evaluate()

    pprint(metrics)
