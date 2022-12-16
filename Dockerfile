FROM ubuntu:18.04

RUN apt-get update && apt-get install -y gcc musl-dev g++
RUN apt-get install -y python3 python3-dev python3-pip

RUN python3 -m pip install pip --upgrade

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

WORKDIR /root
RUN pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_trf-3.4.1/en_core_web_trf-3.4.1.tar.gz --no-deps

COPY config.yaml .
COPY train.sh .
RUN chmod +x train.sh
COPY evaluate_model.py .
RUN mkdir -p data/
RUN mkdir -p models/
