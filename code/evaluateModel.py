import os
import json

import logging

import socket

import spacy

import labelConversion

logpath = "parse_ner.log"

logging.basicConfig(level=logging.DEBUG,
        filename=logpath,
        format='%(asctime)s PID:%(process)d LEVEL:%(levelname)s: %(message)s'
        )

logging.info("Loading model-best")

ner = spacy.load("models/model-best")

logging.info("Setting UP socket ...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 5566))

logging.info("Listening on 127.0.0.1:5566")
s.listen(1)

while True:
    logging.info("Waiting for connection on 127.0.0.1:5566")
    conn, addr = s.accept()
    logging.info("Got connection from %s", addr)

    binaryData = b''

    while 1: 
        data = conn.recv(1024)
        if not data:
            break
        binaryData += data 

    evalData = binaryData.decode("utf-8")

    def getWord(line):
        lineData = line.split()
        if len(lineData) > 0:
            return lineData[0]
        return line

    #Converting from conll2003 data format to plain txt
    evalRecord = " ".join(map(getWord, evalData.split("\n")))
    logging.info("Received record for evaluation %s with len: %d", evalData, len(evalData))

    doc = ner(evalRecord)
    logging.info("processing ner..")

    output = []
    for tok in doc:
        label = tok.ent_iob_
        if label != "O":
            ent = labelConversion.convert2AcharyaLabel(tok.ent_type_)
            label += '-' + ent 
        output.append("\t".join([str(tok), label]))

    logging.info(output)
    conn.sendall("\n".join(output).encode("utf-8"))

    logging.info("Sent output done with the record")
    conn.close()

