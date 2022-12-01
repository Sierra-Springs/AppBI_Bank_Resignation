# SVM, KNN, Naive Bayes, +1 libre
# Découper les données en apprentissage = {train, dev}, validation, test
# Ré-équilibrer les classes (pondération des erreurs ou génération de données)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from pprint import pprint

from Data.DataProvider import *
from Models.SVM import *
from Models.KNN import *

if __name__ == '__main__':
    DataProvider.set_percents(.60, .20, .20)
    dataProvider = SVMDataProvider()

    # svmBase = SVMBaseNoWeights(dataProvider)
    svmBase = SVMBaseAutoWeights(dataProvider)
    svmBase.train()
    metrics = svmBase.evaluate()

    pprint(metrics)

    magentaprint("-" * 30)

    dataProvider = KNNDataProvider()

    # knnBase = KNNBaseUniformWeights(dataProvider)
    knnBase = KNNBaseDistanceWeights(dataProvider)
    knnBase.train()
    metrics = knnBase.evaluate()

    pprint(metrics)
