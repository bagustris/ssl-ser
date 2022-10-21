import os
from os.path import basename, splitext, join as path_join
import sys
import re
import json
from librosa.util import find_files
import pandas as pd

LABEL_DIR_PATH = 'Labels'
WAV_DIR_PATH = 'Audios'


def get_wav_paths_podcast(paths):
    wav_paths = find_files(paths)
    wav_dict = {}
    for wav_path in wav_paths:
        wav_name = splitext(basename(wav_path))[0]
        wav_dict[wav_name] = wav_path
    return wav_dict

def preprocess(data_dirs, paths, wav_paths, out_path):
    meta_data = []
    for idx, row in paths.iterrows():
        if row['EmoClass'] not in ['A', 'H', 'N', 'S']:
            continue
        # remove outlier (stereo, 44.1 kHz)
        if row['FileName'] == 'MSP-PODCAST_1023_0235.wav':
            continue
        filename = row['FileName'][:-4]
        label = row['EmoClass']
        for r in (('A', 'ang'), ('H', 'hap'), 
                ('N', 'neu'), ('S', 'sad')):
            label = label.replace(*r)
        meta_data.append({
                    'path': wav_paths[filename],
                    'label': label
                    })
    data = {
        'labels': {'neu': 0, 'hap': 1, 'ang': 2, 'sad': 3},
        'meta_data': meta_data
    }
    with open(out_path, 'w') as f:
        json.dump(data, f)


def main(data_dir):
    """Main function."""
    out_dir = os.path.join(data_dir, 'meta_data')
    wav_paths = get_wav_paths_podcast(path_join(f"{data_dir}/{WAV_DIR_PATH}"))
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(f"{out_dir}", exist_ok=True)
    data = pd.read_csv(path_join(f"{data_dir}/{LABEL_DIR_PATH}",
                                       'labels_concensus.csv'))
    # Train and test1 1 are used for test
    train_path = data.loc[
        (data.Split_Set == 'Train') | (data.Split_Set == 'Test2')]
    # Using test2 as test
    test_path = data.loc[
        (data['Split_Set'] == 'Test1')]  
    preprocess(data_dir, train_path, wav_paths, 
               path_join(f"{out_dir}", 'train_meta_data.json'))
    preprocess(data_dir, test_path, wav_paths, 
               path_join(f"{out_dir}", 'test_meta_data.json'))


if __name__ == "__main__":
    """input the argument when calling this file
    e.g. python PODCAST_preprocess /path/to/PODCAST"""
    main(sys.argv[1])
