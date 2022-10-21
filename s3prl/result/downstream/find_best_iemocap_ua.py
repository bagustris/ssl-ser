from sklearn.metrics import balanced_accuracy_score
import pandas as pd

upstream="fbank apc_960hr vq_apc_960hr npc_960hr mockingjay_960hr tera_960hr modified_cpc wav2vec_large vq_wav2vec_kmeans wav2vec2_base_960 wav2vec2_large_ll60k wav2vec2_xlsr hubert_base hubert_large_ll60k unispeech_sat_base unispeech_sat_base_plus unispeech_sat_large wavlm_base wavlm_base_plus wavlm_large"

for i in upstream.split(' '):
    # print(f"{i}")
    pred = pd.read_csv(f'iemocap-{i}'+'/'+'test_fold5_predict.txt', 
                       delimiter=' ', header=None)
    pred = pred[1]
    true = pd.read_csv(f'iemocap-{i}'+'/'+'test_fold5_truth.txt', 
                       delimiter=' ', header=None)
    true = true[1]

    # confusion_matrix(true, pred, labels=["ang", "sad", "joy", "neu"])
    # wa = accuracy_score(true, pred)
    ua = balanced_accuracy_score(true, pred)
    print(f"iemocap-{i}: {ua}")
