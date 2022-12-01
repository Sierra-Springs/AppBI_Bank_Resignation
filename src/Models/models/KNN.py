from sklearn.neighbors import KNeighborsClassifier
from Models.Model import Model


class KNN(Model):
    pass


class SVMBaseNoWeights(KNN):
    def __init__(self, data):
        super().__init__(KNeighborsClassifier(), data)


class SVMBaseAutoWeights(KNN):
    def __init__(self, data):
        super().__init__(KNeighborsClassifier(weights="distance"), data)
