FROM nvidia/cuda:11.4.2-devel-ubuntu20.04

RUN apt-get update && apt-get install -y gcc musl-dev g++
RUN apt-get install -y python3 python3-dev python3-pip

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

WORKDIR /root
RUN python3 -m spacy download en_core_web_trf

COPY config.yaml .
COPY train.sh .
RUN chmod +x train.sh
COPY evaluate_model.py .
RUN mkdir -p data/
RUN mkdir -p models/
