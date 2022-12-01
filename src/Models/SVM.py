from sklearn import svm
from Models.Model import Model

class SVM(Model):
    pass


class SVMBaseNoWeights(SVM):
    def __init__(self, data):
        super().__init__(svm.SVC(gamma="scale", verbose=1), data)


class SVMBaseAutoWeights(SVM):
    def __init__(self, data):
        super().__init__(svm.SVC(gamma="scale", class_weight="balanced", verbose=1), data)
