#!/usr/bin/env bash

upstream="fbank apc_960hr vq_apc_960hr npc_960hr mockingjay_960hr tera_960hr modified_cpc wav2vec_large vq_wav2vec_kmeans wav2vec2_base_960 wav2vec2_large_ll60k wav2vec2_xlsr hubert_base hubert_large_ll60k unispeech_sat_base unispeech_sat_base_plus unispeech_sat_large wavlm_base wavlm_base_plus wavlm_large"

#upstream="wavlm_base"
for i in $upstream; do
    echo "Running $i"
    python run_downstream.py -d improv -m train -n improv-$i -u $i -r
done
