from sklearn.naive_bayes import CategoricalNB
from Models.Model import Model


class NaiveBayes(Model):
    pass


class NaiveBayesBase(NaiveBayes):
    def __init__(self, data):
        super().__init__(CategoricalNB(), data)