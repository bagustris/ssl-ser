#!/usr/bin/env python3
import numpy as np
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='Calculate weighted accuracy of mosei. \n Example: ./calc_mosei.py result/downstream/mosei-wavlm/ \n Author: b-atmaja@aist.go.jp', formatter_class=RawTextHelpFormatter)
parser.add_argument('result', type=str, help='prediction directory')
args = parser.parse_args()

pred_file = args.result + 'test_predict.txt'
true_file = args.result + 'test_truth.txt'

pred = np.loadtxt(pred_file)
true = np.loadtxt(true_file)
acc = np.mean(pred == true)
print(f"Weighted accuracy: {acc}")
