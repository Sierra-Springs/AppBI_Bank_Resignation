from sklearn.neural_network import MLPClassifier
from Models.Model import Model


class MLP(Model):
    pass


class MLPBase(MLP):
    def __init__(self, data_provider):
        super().__init__(MLPClassifier(solver='lbfgs',
                                       alpha=1e-5,
                                       hidden_layer_sizes=(5, 2),
                                       random_state=1,
                                       max_iter=1000),
                         data_provider)
