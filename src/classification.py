# SVM, KNN, Naive Bayes, +1 libre
# Découper les données en apprentissage = {train, dev}, validation, test
# Ré-équilibrer les classes (pondération des erreurs ou génération de données)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from pprint import pprint

from Data.DataProvider import DataProvider
from Models.SVM import *

if __name__ == '__main__':
    dataProvider = DataProvider()
    data = dataProvider.get_data_prepare(.60, .20, .20)



    svmBase = SVMBaseNoWeights(data)
    svmBase.train()
    metrics = svmBase.evaluate()

    pprint(metrics)