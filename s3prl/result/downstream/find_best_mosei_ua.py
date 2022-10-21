from sklearn.metrics import accuracy_score, balanced_accuracy_score
from sklearn.metrics import confusion_matrix
import pandas as pd

upstream="fbank apc_960hr vq_apc_960hr npc_960hr mockingjay_960hr tera_960hr modified_cpc wav2vec_large vq_wav2vec_kmeans wav2vec2_base_960 wav2vec2_large_ll60k wav2vec2_xlsr hubert_base hubert_large_ll60k unispeech_sat_base unispeech_sat_base_plus unispeech_sat_large wavlm_base wavlm_base_plus wavlm_large"

for i in upstream.split(' '):
    # print(f"{i}")
    pred = pd.read_csv(f'mosei-{i}'+'/'+'test_predict.txt', header=None)
    # pred = pred[1]
    true = pd.read_csv(f'mosei-{i}'+'/'+'test_truth.txt', header=None)
    # true = true[1]

    confusion_matrix(true, pred)
    wa = accuracy_score(true, pred)
    ua = balanced_accuracy_score(true, pred)
    print(f"moisei-{i}: {ua}")

# emotion
# 0: happy, 1: sad, 2:anger, 3:surprise, 4:disgust, 5;fear
