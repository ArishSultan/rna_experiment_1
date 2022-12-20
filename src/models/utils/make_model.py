from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report


def make_model(name: str, variant):
    match name:
        case 'linear_svm':
            return LinearSVC(**variant)
