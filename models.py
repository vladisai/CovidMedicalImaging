import numpy as np

from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import data


class Model:
    N_CLASSES = 14

    def fit(self, data):
        pass

    def predict(self, data):
        pass


class Baseline(Model):
    def predict(self, x):
        return np.zeros_like(x['lab'])


class SafeOneClassMixin:
    """A hack mixin required to make
    the sklearn classifirs work with training data where for some
    classes we get all training samples with label 0.
    Maybe remove those classes?
    """

    def fit(self, X, y, **kw):
        self._single_class = False
        if len(np.unique(y)) == 1:
            self._single_class = True
            self.classes_ = np.unique(y)
            return self
        return super().fit(X, y, **kw)

    def predict(self, X):
        if self._single_class:
            return np.full(len(X), self.classes_[0])
        return super().predict(X)

    def predict_proba(self, X):
        if self._single_class:
            result = np.zeros((len(X), 2))
            result[:, self.classes_.astype(np.int)[0]] = 1
            return result
        return super().predict_proba(X)


class LogisticRegression(Model):
    class SafeOneClassLogisticRegression(SafeOneClassMixin, LogisticRegression):
        pass

    def fit(self, X, y):
        self.model = MultiOutputClassifier(
            self.SafeOneClassLogisticRegression()).fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def predict(self, X):
        return self.model.predict(X)


class KNeighborsClassifier(Model):
    class SafeOneClassKNN(SafeOneClassMixin, KNeighborsClassifier):
        pass

    def fit(self, X, y):
        self.model = MultiOutputClassifier(self.SafeOneClassKNN()).fit(X, y)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
    def predict(self,X):
        return self.model.predict(X)

class SVC(Model):
    class SafeOneClassSVM(SafeOneClassMixin, SVC):
        pass
    def fit(self,X,y):
        self.model = MultiOutputClassifier(self.SafeOneClassSVM()).fit(X,y)
    def predict(self,X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

class DecisionTreeClassifier(Model):
    class SafeOneClassDT(SafeOneClassMixin, DecisionTreeClassifier):
        pass 
    def fit(self,X,y):                                                                                                   
        self.model = MultiOutputClassifier(self.SafeOneClassDT()).fit(X,y)
    def predict(self,X): 
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
class RandomForestClassifier(Model):
    class SafeOneClassRF(SafeOneClassMixin, RandomForestClassifier):
        pass 
    def fit(self,X,y):                                                                                                   
        self.model = MultiOutputClassifier(self.SafeOneClassRF()).fit(X,y)
    def predict(self,X): 
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
class AdaBoostClassifier(Model):
    class SafeOneClassAB(SafeOneClassMixin, AdaBoostClassifier):
        pass 
    def fit(self,X,y):                                                                                                   
        self.model = MultiOutputClassifier(self.SafeOneClassAB()).fit(X,y)
    def predict(self,X): 
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
class GaussianNB(Model):
    class SafeOneClassNB(SafeOneClassMixin, GaussianNB):
        pass 
    def fit(self,X,y):                                                                                                   
        self.model = MultiOutputClassifier(self.SafeOneClassNB()).fit(X,y)
    def predict(self,X): 
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

class QuadraticDiscriminantAnalysis(Model):
    class SafeOneClassQDA(SafeOneClassMixin, QuadraticDiscriminantAnalysis):
        pass 
    def fit(self,X,y):                                                                                                   
        self.model = MultiOutputClassifier(self.SafeOneClassQDA()).fit(X,y)
    def predict(self,X): 
        return self.model.predict(X)
    def predict_proba(self, X):
        return self.model.predict_proba(X)
