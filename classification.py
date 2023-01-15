# SVM, KNN, Naive Bayes, +1 libre
# Découper les données en apprentissage = {train, dev}, validation, test
# Ré-équilibrer les classes (pondération des erreurs ou génération de données)

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from pprint import pprint
from datetime import datetime

from Data.DataProvider import *
from Models.SVM import *
from Models.KNN import *
from Models.NaiveBayes import *
from Models.MLP import *
from Models.CometMLManager import CometMLManager

if __name__ == '__main__':
    date_now_str = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")  # Do not put any space in the format, here
    print(date_now_str)
    input()

    cometMLManager = CometMLManager()  # Gestionnaire d'expérience et de modèles
    cometMLManager.start_experiment(f"ModelsTest_{date_now_str}")  # Nouvelle expérience
    DataProvider.set_percents(.60, .20, .20)

    # liste des modèles à tester
    models = [SVMBaseAutoWeights(SVMDataProvider()),
              KNNBaseDistanceWeights(KNNDataProvider()),
              NaiveBayesBase(NaiveBayesDataProvider()),
              MLPBase(SVMDataProvider())]

    models = [MLPBase(SVMDataProvider())]

    all_metrics = dict()  # Métriques de tous les modèles
    for model in models:
        magentaprint("_" * 30)
        magentaprint(f"Model : {model.name}")
        model.train()
        metrics = model.evaluate()

        # Enregistrement du modèle complet dans un fichier
        model_path = cometMLManager.save_model_to_file(model=model, model_name="NaiveBayesBase")
        # Enregistrement du modèle (du fichier) vers l'expérience CometML
        cometMLManager.log_model(_model_name="NaiveBayesBase")

        pprint(metrics)

        all_metrics[model.name] = metrics

    # log des metriques sur CometML
    cometMLManager.log_metrics(all_metrics)
