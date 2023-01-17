from sklearn.neighbors import KNeighborsClassifier
from Models.Model import Model


class KNN(Model):
    KEY_N_NEIGHBORS = "n_neighbors"

    def __init__(self, data_provider, params=None):
        if params is None:
            params = dict()
        if hasattr(self, "params"):
            for key in self.params:
                assert key not in params, f"{key}=\"{self.params[key]}\" in {self.__class__.__name__}" \
                                          f" and can not be redefined"
                params[key] = self.params[key]
        super().__init__(KNeighborsClassifier, data_provider, params)

    def auto_name(self, name):
        super().auto_name(name)
        super().auto_name(self.name + "__" + "_".join([str(i) for i in [1, 2, 3]]))


class KNNBaseUniformWeights(KNN):
    def __init__(self, data_provider, params=None):
        self.params = {"weights": "uniform"}
        super().__init__(data_provider, params)


class KNNBaseDistanceWeights(KNN):
    def __init__(self, data_provider, params=None):
        self.params = {"weights": "distance"}
        super().__init__(data_provider, params)


if __name__ == '__main__':
    from Data.DataProvider import MartineDataProvider
    kn = KNNBaseUniformWeights(MartineDataProvider(), params={KNN.KEY_N_NEIGHBORS: 2})
    print(kn.name)
    print(kn.clf.n_neighbors)