import os
from os.path import basename, splitext, join as path_join
import sys
import re
import json
from librosa.util import find_files

# LABEL_DIR_PATH = 'dialog/EmoEvaluation'
# WAV_DIR_PATH = 'sentences/wav'


def get_wav_paths(data_dirs):
    wav_paths = find_files(data_dirs)
    wav_dict = {}
    for wav_path in wav_paths:
        wav_name = splitext(basename(wav_path))[0]
        start = wav_path.find('session')
        wav_path = wav_path[start:]
        wav_dict[wav_name] = wav_path

    return wav_dict


def preprocess(data_dirs, paths, out_path):
    meta_data = []
    for path in paths:
        wav_paths = get_wav_paths(path_join(data_dirs, path))
        label_dir = path_join(data_dirs)
        # label_paths = list(os.listdir(label_dir))
        # label_paths = [label_path for label_path in label_paths
        #                if splitext(label_path)[1] == '.txt']
        # for label_path in label_paths:
        label_path = 'Evaluation.txt'
        with open(path_join(label_dir, label_path)) as f:
            for line in f:
                if line[:3] != 'UTD':
                    continue
                line = line.split(';')
                if line[1].lstrip() not in ['A', 'H', 'N', 'S']:
                    continue
                filename = 'MSP-' + line[0][4:-4]
                if filename not in wav_paths:
                    continue
                meta_data.append({
                        'path': wav_paths[filename],
                        'label': line[1].strip()
                        })
    data = {
        'labels': {'A': 0, 'H': 1, 'N': 2, 'S': 3},
        'meta_data': meta_data
    }
    with open(out_path, 'w') as f:
        json.dump(data, f)


def main(data_dir):
    """Main function."""
    paths = list(os.listdir(data_dir))
    paths = [path for path in paths if path[:7] == 'session']
    paths.sort()
    out_dir = os.path.join(data_dir, 'meta_data')
    os.makedirs(out_dir, exist_ok=True)
    for i, path in enumerate(paths):
        os.makedirs(f"{out_dir}/{path}", exist_ok=True)
        preprocess(data_dir, paths[:i] + paths[i + 1:], 
                path_join(f"{out_dir}/{path}", 'train_meta_data.json'))
        preprocess(data_dir, [path], path_join(
            f"{out_dir}/{path}", 'test_meta_data.json'))


if __name__ == "__main__":
    main(sys.argv[1])
