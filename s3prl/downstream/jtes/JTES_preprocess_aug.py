#!/usr/bin/env python3
import sys
import glob
import os
import json


def main(data_dir):
    file = glob.glob(os.path.join(data_dir + 'wav/*/*/', '*.wav'))
    file_glt = glob.glob(os.path.join(data_dir + 'arhmm/*/*/', '*_glt.wav'))
    file_spc = glob.glob(os.path.join(data_dir + 'arhmm/*/*/', '*_spc.wav'))
    # file_ir = glob.glob(os.path.join(data_dir + 'aug_ir/*/*/', '*.wav'))
    file_noi = glob.glob(os.path.join(data_dir + 'aug_noise/*/*/', '*.wav'))

    # files.extend(files_)
    files = file + file_noi + file_glt + file_spc
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
            # if os.path.basename(file)[-7:-4] == 'glt':
            #     continue
            # if os.path.basename(file)[-7:-4] == 'spc':
            #     continue
            if os.path.basename(file)[10:14] != '.wav': # exclude aug for test
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
    with open(f"{out_dir}/train_meta_data_noi_glt_spc.json", 'w') as f1:
        json.dump(data_train, f1)
    with open(f"{out_dir}/test_meta_data_noi_glt_spc.json", 'w') as f2:
        json.dump(data_test, f2)

    print(f"length data_train: {len(data_train['meta_data'])}")
    print(f"length data_test: {len(data_test['meta_data'])}")

if __name__ == '__main__':
    main(sys.argv[1])