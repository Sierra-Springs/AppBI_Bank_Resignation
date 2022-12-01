from sklearn import svm
from Models.Model import Model


class SVM(Model):
    pass


class SVMBaseNoWeights(SVM):
    def __init__(self, data_provider):
        super().__init__(svm.SVC(gamma="scale", verbose=1), data_provider)


class SVMBaseAutoWeights(SVM):
    def __init__(self, data_provider):
        super().__init__(svm.SVC(gamma="scale", class_weight="balanced", verbose=1), data_provider)
