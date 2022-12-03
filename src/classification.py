# SVM, KNN, Naive Bayes, +1 libre
# Découper les données en apprentissage = {train, dev}, validation, test
# Ré-équilibrer les classes (pondération des erreurs ou génération de données)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from pprint import pprint

from Data.DataProvider import *
from Models.SVM import *
from Models.KNN import *
from Models.NaiveBayes import *
from Models.CometMLManager import CometMLManager

if __name__ == '__main__':
    cmm = CometMLManager()
    cmm.start_experiment("ModelsTest")
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

    magentaprint("-" * 30)






    dataProvider = NaiveBayesDataProvider()

    model = NaiveBayesBase(dataProvider)
    model.train()

    model_path = cmm.save_model_to_file(model=model, model_name="NaiveBayesBase")
    cmm.log_model(_model_name="NaiveBayesBase")
    metrics = model.evaluate()
    cmm.log_metrics(metrics)

    pprint(metrics)
