# importing necessary libraries
from Models.CometModelManager import CometModelManager
from sklearn import datasets
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import numpy as np
import joblib


def continuer():
    answ = input("continuer ? (y/n): ")
    while not answ in ['y', 'n']:
        print("Choix incorrect")
        answ = input("continuer ? (y/n): ")
    if answ == 'n':
        exit()


def test_classifier(clf):
    preds = clf.predict(X_test)
    a_good_pred_index = np.where(preds == y_test)[0][0]
    a_bad_pred_index = np.where(preds != y_test)[0][0]
    print("a_good_pred_index", a_good_pred_index)
    print(X_test[a_good_pred_index], "pred:", preds[a_good_pred_index], "vraie classe:", y_test[0])
    print(X_test[a_bad_pred_index], "pred:", preds[a_bad_pred_index], "vraie classe:", y_test[0])
    print("Prédictions juste:", (preds == y_test).sum(), "/", len(y_test))
    cm = confusion_matrix(y_test, preds)
    print("matrice de confusion:")
    print(cm)


if __name__ == '__main__':
    # loading the iris dataset
    iris = datasets.load_iris()

    # X -> features, y -> label
    X = iris.data
    y = iris.target

    # dividing X, y into train and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

    # training a DescisionTreeClassifier
    from sklearn.tree import DecisionTreeClassifier
    model = DecisionTreeClassifier(max_depth = 2)
    model.fit(X_train, y_train)

    cmm = CometModelManager()
    print("Enregistrement du modèle en local")
    model_path = cmm.sklearn_model_to_file(sklearn_model=model, model_name="iris-model") # enregistre le model
    print("chargement du modèle enregistré en local")
    clf = cmm.file_to_sklear_model(model_name="iris-model") # recharge le model depuis le fichier


    print(10 * "_" + "Classifieur originel" + 10 * "_")
    test_classifier(clf)

    print()
    print("modèle original enregistré sous: " + model_path)
    print()

    continuer()
    print()
    print("log du modèle dans les expériences comet")
    cmm.log_model(_model_name="iris-model")

    print("Récupération du model depuis les expériences comet_ML")
    clf = cmm.download_model_from_experiment("iris-model")

    print(10 * "_" + "Classifieur récupéré des expériences Comet" + 10 * "_")
    test_classifier(clf)

    print()
    continuer()
    print()

    print("enregistrement du model dans Model Registry sur Comet ML pour les model intéressants")
    cmm.register_model("iris-model")



    print("récupération du model depuis Model Registry")
    clf = cmm.download_model("iris-model")

    print(10 * "_" + "Classifieur récupéré de Model Registry" + 10 * "_")
    test_classifier(clf)
