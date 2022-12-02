from sklearn.neighbors import KNeighborsClassifier
from Models.Model import Model


class KNN(Model):
    pass


class KNNBaseUniformWeights(KNN):
    def __init__(self, data_provider):
        super().__init__(KNeighborsClassifier(), data_provider)


class KNNBaseDistanceWeights(KNN):
    def __init__(self, data_provider):
        super().__init__(KNeighborsClassifier(weights="distance"), data_provider)
