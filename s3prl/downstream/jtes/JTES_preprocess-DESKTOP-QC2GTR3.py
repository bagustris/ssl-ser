#!/usr/bin/env python3
import sys
import glob
import os
import json


def main(data_dir):
    file = glob.glob(os.path.join(data_dir + 'wav/*/*/', '*.wav'))
    files_glt = glob.glob(os.path.join(data_dir + 'arhmm/*/*/', '*_glt.wav'))
    files = file + files_glt
    files.sort()

    data_train = []
    data_test = []
    # data_val = []

    for file in files:
        # processing file
        print("Processing... ", file)
        lab_str = os.path.basename(os.path.dirname(file))
        # use speaker 1-45 and text 1-40 as training, the rest as test
        if int(os.path.basename(file)[1:3]) in range(1, 46):
            if int(os.path.basename(file)[8:10]) in range(1, 41):
                data_train.append({
                    "path": file,
                    "label": lab_str,
                    "speaker": int(os.path.basename(file)[1:3]),
                })

        elif int(os.path.basename(file)[1:3]) in range(46, 51): # = else:
            if os.path.basename(file)[-7:-4] == 'glt':
                continue
            if os.path.basename(file)[-7:-4] == 'spc':
                continue
            if int(os.path.basename(file)[8:10]) in range(41, 51):
                data_test.append({
                    "path": file,
                    "label": lab_str,
                    "speaker": int(os.path.basename(file)[1:3]),
                })

    out_dir = os.path.join(data_dir, 'meta_data')
    os.makedirs(out_dir, exist_ok=True)
    data_train = {
        'labels': {'ang': 0, 'joy': 1, 'neu': 2, 'sad': 3},
        'meta_data': data_train
    }
    data_test = {
        'labels': {'ang': 0, 'joy': 1, 'neu': 2, 'sad': 3},
        'meta_data': data_test
    }
    with open(f"{out_dir}/train_meta_data_glt.json", 'w') as f1:
        json.dump(data_train, f1)
    with open(f"{out_dir}/test_meta_data_glt.json", 'w') as f2:
        json.dump(data_test, f2)


if __name__ == '__main__':
    main(sys.argv[1])