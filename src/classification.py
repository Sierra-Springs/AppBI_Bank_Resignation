# SVM, KNN, Naive Bayes, +1 libre
# Découper les données en apprentissage = {train, dev}, validation, test
# Ré-équilibrer les classes (pondération des erreurs ou génération de données)


from sklearn import svm
from sklearn.dummy import DummyClassifier
from sklearn.metrics import confusion_matrix

from Data.DataProvider import DataProvider
from Utils.pathsDefinition import *
from Utils.ColorPrinter import *
from Utils.names import *

import pandas as pd

if __name__ == '__main__':
    print(table1Path)
    dataProvider = DataProvider()
    data = dataProvider.get_data_prepare(.60, .20, .20)

    for key in data.keys():
        blueprint(key)
        print(data[key]["X"])
        print()

    clfs = [svm.SVC(gamma="scale"), DummyClassifier()]
    clfs_names = ["svm", "dummy"]

    for clf, clf_name in zip(clfs, clfs_names):

        clf.fit(data[TRAIN]["X"], data[TRAIN]["Y"])

        print('Accuracy of ' + clf_name + ' classifier on training set: {:.2f}'
              .format(clf.score(data[TRAIN]["X"], data[TRAIN]["Y"])))

        print('Accuracy of ' + clf_name + ' classifier on valid set: {:.2f}'
              .format(clf.score(data[VALID]["X"], data[VALID]["Y"])))

        print('Accuracy of ' + clf_name + ' classifier on test set: {:.2f}'
              .format(clf.score(data[TEST]["X"], data[TEST]["Y"])))

        y_pred = clf.predict(data[VALID]["X"])
        print(confusion_matrix(data[VALID]["Y"], y_pred))

        y_pred = clf.predict(data[TEST]["X"])
        print(confusion_matrix(data[TEST]["Y"], y_pred))

        blueprint("_" * 30)