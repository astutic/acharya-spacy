FROM ubuntu:20.04

RUN apt-get update && apt-get install -y gcc musl-dev g++
RUN apt-get install -y python3 python3-dev python3-pip

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

WORKDIR /root
COPY configs/ .
COPY code/ .
RUN chmod +x code/*
RUN mkdir -p data/
RUN mkdir -p models/

