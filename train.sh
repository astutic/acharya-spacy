#!/bin/sh

echo "Download en_core_web_trf spacy model"

python3 -m spacy download en_core_web_trf

echo "training done..."
