import os
import json

import logging

import socket

import spacy

logpath = "parse_ner.log"

logging.basicConfig(level=logging.DEBUG,
        filename=logpath,
        filemode='w')

logPrefix = "PID:%d:EVAL::" % os.getpid()

logging.info(logPrefix + "Setting UP socket ...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 5566))

logging.info(logPrefix + "Listening on 127.0.0.1:5566")
s.listen(1)

ner = spacy.load("models/model-best")

while True:
    logging.info(logPrefix + "Waiting for connection on 127.0.0.1:5566")
    conn, addr = s.accept()
    logging.info(logPrefix + "Got connection from %s", addr)

    binaryData = b''

    while 1: 
        data = conn.recv(1024)
        if not data:
            break
        binaryData += data 

    evalData = binaryData.decode("utf-8")
    logging.info(logPrefix + "Received record for evaluation with len: %d", len(evalData))

    #Converting from conll evaluation data to plain txt
    evalRecord = " ".join(evalData.split("\n"))

    doc = ner(evalRecord)
    logging.info(logPrefix + "processing ner..")

    entities = [[ent.start_char, ent.end_char, ent.label_, ent.text] for ent in doc.ents]
    output = [e[0:3] for e in entities]

    conn.sendall(json.dumps(output).encode("utf-8"))
    logging.info(output)
    logging.info(logPrefix + "Sent output done with the record")
    conn.close()


