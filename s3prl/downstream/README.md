# serdata
A data pre-processing toolkit intended to standardize evaluation of speech emotion recognition datasets


The intent of this repository is to standardize evaluation method (i.e., "test set") for speech emotion recognition. A huge number of authors reported their paper under different conditions. Hence, it is difficult to justify "which method performs better under the same test condition". 

The basic idea of this toolkit is based on the following two premises:  

```
1. You can utilize any training data, any method, including data augmentation and and pre-trained model to support you claim as long as you follow step (2).
2. The test data provided here *must not be included* in training data (1), nor be augmented for training data.
```

## Structure
A new datasets configuration should be located in this `downstream` directory. 

## Raw data
Unlike datasets library (Tensorflow datasets, huggingface's datasets, Pytorch datasets), we require a raw data for data proccessing. Hence, the user can experiment with differenct format (.wav, .flac, .mp3) for augmentation or others.


## Already Supported datasets
- [IEMOCAP](https://sail.usc.edu/iemocap/)  
- [JTES](https://doi.org/10.1109/ICSDA.2016.7918977)  
- [CMU-MOSEI](http://multicomp.cs.cmu.edu/resources/cmu-mosei-dataset/)  
- [MSP-IMPROV](https://ecs.utdallas.edu/research/researchlabs/msp-lab/MSP-Improv.html)  
- [MSP-PODCAST](https://ecs.utdallas.edu/research/researchlabs/msp-lab/MSP-Podcast.html)  

## Planned datasets
- [AESDD](http://m3c.web.auth.gr/research/aesdd-speech-emotion-recognition/)
- [CaFE](https://zenodo.org/record/1478765)
- [CREMA-D](https://github.com/CheyneyComputerScience/CREMA-D), [AudioWAV only](https://www.kaggle.com/ejlok1/cremad)
- [DEMoS](https://zenodo.org/record/2544829)
- [EMO-DB](http://emodb.bilderbar.info/)
- [EmoFilm](https://zenodo.org/record/1326428)
- [EmoryNLP](https://github.com/declare-lab/MELD/)
- [EmoV-DB](https://github.com/numediart/EmoV-DB)
- [EMOVO](http://voice.fub.it/activities/corpora/emovo/index.html)
- [ESD](https://hltsingapore.github.io/ESD/)
- [eNTERFACE](http://www.enterface.net/results/)
- [JL-corpus](https://www.kaggle.com/tli725/jl-corpus)
- [MELD](https://github.com/declare-lab/MELD/)
- [0GVC](http://research.nii.ac.jp/src/en/OGVC.html)
- [Portuguese](https://link.springer.com/article/10.3758/BRM.42.1.74)
- [RAVDESS](https://zenodo.org/record/1188976)
- [SAVEE](http://kahlan.eps.surrey.ac.uk/savee/)
- [SEMAINE](https://semaine-db.eu/)
- [ShEMO](https://github.com/mansourehk/ShEMO)
- [SmartKom](https://clarin.phonetik.uni-muenchen.de/BASRepository/index.php)
- [SUBESCO](https://zenodo.org/record/4526477)
- [TESS](https://tspace.library.utoronto.ca/handle/1807/24487/)
- [URDU](https://github.com/siddiquelatif/URDU-Dataset/)
- [UUDB](http://research.nii.ac.jp/src/en/UUDB.html)
- [VENEC](https://www.nature.com/articles/s41562-019-0533-6)

## S3PRL
https://github.com/s3prl/s3prl
