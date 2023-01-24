#!/bin/sh

echo "converting conll datafile to spacy DocBin..."

python3 -m spacy convert data/trainfile.conll data/ -c conll

echo "initializing config..."
#python3 -m spacy init config - --gpu --lang hi --pipeline ner --optimize accuracy | python3 -m spacy train - --output models/ --paths.train ./data/trainfile.spacy --paths.dev ./data/trainfile.spacy --gpu-id 0
python3 -m spacy init fill-config base_config.cfg config.cfg
echo "begin training..."
python3 -m spacy train config.cfg --output models/ --paths.train ./data/trainfile.spacy --paths.dev ./data/trainfile.spacy --gpu-id 0

echo "training done..."
