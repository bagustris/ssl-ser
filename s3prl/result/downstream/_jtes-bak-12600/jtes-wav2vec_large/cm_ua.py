from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import balanced_accuracy_score
import pandas as pd

pred = pd.read_csv('test_fold1_predict.txt', delimiter=' ', header=None)
pred = pred[1]
true = pd.read_csv('test_fold1_truth.txt', delimiter=' ', header=None)
true = true[1]

confusion_matrix(true, pred, labels=["ang", "sad", "joy", "neu"])
wa = accuracy_score(true, pred)
ua = balanced_accuracy_score(true, pred)