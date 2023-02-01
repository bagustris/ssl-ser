#!/usr/bin/env python3

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='Plot CM of mosei. \n Example: ./plot_cm.py result/downstream/mosei-wavlm/ \n Author: b-atmaja@aist.go.jp', formatter_class=RawTextHelpFormatter)
parser.add_argument('result', type=str, help='prediction directory')
args = parser.parse_args()

pred_file = args.result + 'test_predict.txt'
true_file = args.result + 'test_truth.txt'

pred = np.loadtxt(pred_file)
true = np.loadtxt(true_file)

cm = confusion_matrix(true, pred, normalize='true')
disp = ConfusionMatrixDisplay(confusion_matrix=cm, 
                              display_labels=['neg', 'neu', 'pos'])
# display_labels=['hap', 'sad', 'ang', 'sur', 'dis', 'fea') 
disp.plot()
# plt.show()
plt.savefig('cm_3.pdf')
