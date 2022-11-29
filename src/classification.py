# SVM, KNN, Naive Bayes, +1 libre
# Découper les données en apprentissage = {train, dev}, validation, test
# Ré-équilibrer les classes (pondération des erreurs ou génération de données)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from pprint import pprint

from Models.SVM import *

if __name__ == '__main__':
    svmBase = SVMBaseNoWeights()
    metrics = svmBase.evaluate()

    pprint(metrics)