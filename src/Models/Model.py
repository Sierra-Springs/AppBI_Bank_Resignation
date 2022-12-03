import sklearn.metrics
from sklearn.metrics import confusion_matrix

from Utils.pathsDefinition import *
from Utils.ColorPrinter import *
from Utils.names import *

import os
import time
import pickle


class Model:
    def __init__(self, clf, data_provider, name=None):
        if isinstance(clf, str):
            self.load_sklearn_model(clf)
        else:
            self.clf = clf
        self.dataProvider = data_provider
        self.data = self.dataProvider.get_data_prepare()
        self.name = self.__class__.__name__ if name is None else name

    def save_sklearn_model(self):
        model_dir = modelsPaths / self.__class__.__bases__[0].__name__ / "sklearn"
        os.makedirs(model_dir, exist_ok=True)
        with open(model_dir / (self.name + ".pkl"), 'wb') as modelFile:
            pickle.dump(self.clf, modelFile)

    def load_sklearn_model(self, modelpath):
        """TODO : Si on instancie un NaiveBayesModel par exemple, on peut load un sklearn model SVM !!
        Crée un ModelLoader qui instancie un Model simple et charge le clf, peut-être"""
        with open(modelpath, 'rb') as modelFile:
            self.clf = pickle.load(modelFile)

    def train(self):
        time_start = time.time()
        blueprint(f"Model fit ({time.time() - time_start:.4}s)")
        self.clf.fit(self.data[TRAIN]["X"], self.data[TRAIN]["Y"])
        self.save_sklearn_model()

    def evaluate(self):
        time_start = time.time()
        blueprint(f"Evaluation du model {self.__class__.__name__}")

        metrics = {"model_name": self.__class__.__name__,
                   "accuracy": dict(),
                   "pre_rec_fscore": dict(),
                   "rocauc": dict(),
                   "confusion_matrix": dict()
                   }

        blueprint(f"Metrics generation ({time.time() - time_start:.4}s)")
        for data_type in [TRAIN, VALID]:
            y_pred = self.clf.predict(self.data[data_type]["X"])

            cyanprint(f"[{data_type}] Accuracy... ({time.time() - time_start:.4}s)")
            metrics["accuracy"][data_type] = self.clf.score(self.data[data_type]["X"], self.data[data_type]["Y"])

            cyanprint(f"[{data_type}] Precision Recall f-score... ({time.time() - time_start:.4}s)")
            metrics["pre_rec_fscore"][data_type] = dict()
            for average in [None, "weighted"]:
                prfs = sklearn.metrics.precision_recall_fscore_support(self.data[data_type]["Y"], y_pred, average=average)
                metrics["pre_rec_fscore"][data_type][str(average)] = dict()
                metrics["pre_rec_fscore"][data_type][str(average)]["precision"] = prfs[0]
                metrics["pre_rec_fscore"][data_type][str(average)]["recall"] = prfs[1]
                metrics["pre_rec_fscore"][data_type][str(average)]["fscore"] = prfs[2]

            cyanprint(f"[{data_type}] Roc-Auc... ({time.time() - time_start:.4}s)")
            metrics["rocauc"][data_type] = dict()
            for average in [None, "weighted", "samples"]:
                rocauc = sklearn.metrics.roc_auc_score(self.data[data_type]["Y"], y_pred, average=average)
                metrics["rocauc"][data_type][str(average)] = rocauc

            cyanprint(f"[{data_type}] Confusion Matrix... ({time.time() - time_start:.4}s)")
            metrics["confusion_matrix"][data_type] = confusion_matrix(self.data[data_type]["Y"], y_pred)

        blueprint(f"Finished ({time.time() - time_start:.4}s)")
        return metrics