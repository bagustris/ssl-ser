import os
import math
import torch
import random

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence

from .model import Model
from .dataset import MOSEIDataset

import pandas as pd
import sys

from collections import defaultdict
import sklearn
from pathlib import Path


class DownstreamExpert(nn.Module):
    """
    Used to handle downstream-specific operations
    eg. downstream forward, metric computation, contents to log
    """

    def __init__(self, upstream_dim, downstream_expert, expdir, **kwargs):
        """
        Args:
            upstream_dim: int
                Different upstream will give different representation dimension
                You might want to first project them to the same dimension
            
            downstream_expert: dict
                The 'downstream_expert' field specified in your downstream config file
                eg. downstream/downstream/example/config.yaml

            **kwargs: dict
                The arguments specified by the argparser in run_downstream.py
                in case you need it.
        """

        super(DownstreamExpert, self).__init__()
        self.upstream_dim = upstream_dim
        self.datarc = downstream_expert['datarc']
        self.modelrc = downstream_expert['modelrc']

        # Convert Label File to (filename, label) for each split
        self.train_data, self.dev_data, self.test_data = [], [], []
        df = pd.read_csv(self.datarc['label_dir'], encoding="latin-1")
        for row in df.itertuples():
            filename = row.file + '_' + str(row.index) + '.wav'
            if self.datarc['num_class'] == 2:
                label = row.label2a
            else:
                label = row.label7 + 3 # Avoid CUDA error: device-side assert triggered (due to negative label)
            if row.split == 0:
                self.train_data.append((filename, label))
            elif row.split == 1:
                self.dev_data.append((filename, label))
            elif row.split == 2:
                self.test_data.append((filename, label))

        self.train_dataset = MOSEIDataset('train', self.train_data, self.datarc['data_dir'])
        self.dev_dataset = MOSEIDataset('dev', self.dev_data, self.datarc['data_dir'])
        self.test_dataset = MOSEIDataset('test', self.test_data, self.datarc['data_dir'])

        self.connector = nn.Linear(upstream_dim, self.modelrc['input_dim'])
        self.model = Model(
            output_class_num=self.datarc['num_class'],
            **self.modelrc
        )
        self.objective = nn.CrossEntropyLoss()
        self.expdir = expdir
        self.logging = os.path.join(self.expdir, 'log.log')
        self.best = defaultdict(lambda: 0)
        self.answer = []

    def _get_train_dataloader(self, dataset):
        return DataLoader(
            dataset, batch_size=self.datarc['train_batch_size'],
            shuffle=True, num_workers=self.datarc['num_workers'],
            collate_fn=dataset.collate_fn
        )

    def _get_eval_dataloader(self, dataset):
        return DataLoader(
            dataset, batch_size=self.datarc['eval_batch_size'],
            shuffle=False, num_workers=self.datarc['num_workers'],
            collate_fn=dataset.collate_fn
        )

    """
    Datalaoder Specs:
        Each dataloader should output a list in the following format:

        [[wav1, wav2, ...], your_other_contents1, your_other_contents2, ...]

        where wav1, wav2 ... are in variable length
        each wav is torch.FloatTensor in cpu with:
            1. dim() == 1
            2. sample_rate == 16000
            3. directly loaded by torchaudio without any preprocessing
    """

    # Interface
    def get_train_dataloader(self):
        return self._get_train_dataloader(self.train_dataset)

    # Interface
    def get_dev_dataloader(self):
        return self._get_eval_dataloader(self.dev_dataset)

    # Interface
    def get_test_dataloader(self):
        return self._get_eval_dataloader(self.test_dataset)

    def get_dataloader(self, mode):
        return eval(f'self.get_{mode}_dataloader')()

    # Interface
    def forward(self, mode, features, labels, filenames, records, **kwargs): 
        """
        This function will be used in both train/dev/test, you can use
        self.training (bool) to control the different behavior for
        training or evaluation (dev/test)

        Args:
            features:
                list of unpadded features [feat1, feat2, ...]
                each feat is in torch.FloatTensor and already
                put in the device assigned by command-line args

            records:
                defaultdict(list), by dumping contents into records,
                these contents can be averaged and logged on Tensorboard
                later by self.log_records

                Note1. downstream/runner.py will call self.log_records
                    1. every log_step during training
                    2. once after evalute the whole dev/test dataloader

                Note2. log_step is defined in your downstream config

            logger:
                Tensorboard SummaryWriter, given here for logging/debugging convenience
                please use f'{prefix}your_content_name' as key name
                to log your customized contents

            prefix:
                used to indicate downstream and train/test on Tensorboard
                eg. 'phone/train-'

            global_step:
                global_step in runner, which is helpful for Tensorboard logging

        Return:
            loss:
                the loss to be optimized, should not be detached
                a single scalar in torch.FloatTensor
        """
        features = pad_sequence(features, batch_first=True)
        features = self.connector(features)
        predicted = self.model(features)

        utterance_labels = labels
        labels = torch.LongTensor(utterance_labels).to(features.device)
        loss = self.objective(predicted, labels)
        predicted_classid = predicted.max(dim=-1).indices
        
        records['acc'] += (predicted_classid == labels).view(-1).cpu().float().tolist()
        records['filename'] += filenames
        records['predicted'] += predicted_classid.cpu().float().tolist()
        records['original'] += labels.cpu().float().tolist()

        if not self.training:
            # some evaluation-only processing, eg. decoding
            pass

        return loss

    # interface
    def log_records(self, mode, records, logger, global_step, **kwargs):
    #def log_records(self, records, logger, prefix, global_step, **kwargs):
        """
        This function will be used in both train/dev/test, you can use
        self.training (bool) to control the different behavior for
        training or evaluation (dev/test)

        Args:
            records:
                defaultdict(list), contents already prepared by self.forward

            logger:
                Tensorboard SummaryWriter
                please use f'{prefix}your_content_name' as key name
                to log your customized contents

            prefix:
                used to indicate downstream and train/test on Tensorboard
                eg. 'phone/train-'

            global_step:
                global_step in runner, which is helpful for Tensorboard logging
        """
        #for key, values in records.items():
        #    average = torch.FloatTensor(values).mean().item()
        #    logger.add_scalar(
        #        f'{prefix}{key}',
        #        average,
        #        global_step=global_step
        #    )
        save_ckpt = []
        
        average = torch.FloatTensor(records['acc']).mean().item()
        f1 = sklearn.metrics.f1_score(records['original'],
                                      records['predicted'],
                                      average="macro")
        logger.add_scalar(
            f"mosei/{mode}-acc",
            average,
            global_step=global_step
        )
      
        with open(self.logging, 'w') as f:
            #print(f'{mode} acc: {average}')
            # print("ERROR")
            message = f'{mode}|step:{global_step}|acc:{average}|f1:{f1}\n'
            f.write(message)

            if mode == 'test' and average > self.best[mode]:
                self.best[mode] = average
                message = f'best|{message}'
                # name = prefix.split('/')[-1].split('-')[0]
                save_ckpt.append(f'best-states-{mode}.ckpt')
                if mode == 'test':
                    with open(Path(self.expdir) / f"{mode}_predict.txt", "w") as file:
                        line = [f"{f} \n" for f in records["predicted"]]
                        file.writelines(line)
        if mode == 'test':
            with open(Path(self.expdir) / f"{mode}_truth.txt", "w") as file:
                line = [f"{f} \n" for f in records["original"]]
                file.writelines(line)
              
        if not self.training:
            # some evaluation-only processing, eg. decoding
            pass
    
        return save_ckpt