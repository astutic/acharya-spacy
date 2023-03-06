#!/bin/bash

echo "converting conll datafile to spacy DocBin..."

python3 -m spacy convert data/trainfile.conll data/ -c conll

echo "initializing config..."

declare -a cfg_params

[[ ! -z $gpu_id ]] && cfg_params+=("--gpu")
[[ ${#lang} == 2 ]] && cfg_params+=("--lang $lang")
[[ "$optimize" == "accuracy" ]] || [[ "$optimize" == "efficiency" ]] && cfg_params+=("--optimize $optimize")

python3 -m spacy init config config.cfg --force --pipeline ner ${cfg_params[@]}

echo "begin training..."

declare -a train_params

[[ ! -z $gpu_id ]] && train_params=("--gpu-id $gpu_id")
python3 -m spacy train config.cfg --output models/ --paths.train ./data/trainfile.spacy --paths.dev ./data/trainfile.spacy ${train_params[@]} 

echo "training done..."

cp NEREntities.json models/
cp config.cfg models/
