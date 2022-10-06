#!/bin/sh

echo "converting conll datafile to spacy DocBin..."

python3 -m spacy convert data/trainfile.conll data/ -c conll

echo "initializing config and begin training..."
python3 -m spacy init config - --gpu --lang en --pipeline ner --optimize accuracy | python3 -m spacy train - --output models/ --paths.train ./data/trainfile.spacy --paths.dev ./data/trainfile.spacy --gpu-id 0

echo "training done..."
