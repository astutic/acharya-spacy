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



# ner = spacy.load("models/model-best")
ner = spacy.load("en_core_web_trf")

ModelLabelsToCONLL = {
    'CARDINAL':'MISC', 
    'DATE':'MISC', 
    'EVENT':'MISC', 
    'FAC':'MISC',
    'GPE':'LOC',
    'LANGUAGE':'MISC',
    'LAW':'MISC',
    'LOC':'LOC',
    'MONEY':'MISC',
    'NORP':'MISC',
    'ORDINAL':'MISC',
    'ORG':'ORG',
    'PERCENT':'O',
    'PERSON':'PER',
    'PRODUCT':'MISC',
    'QUANTITY':'O',
    'TIME':'O',
    'WORK_OF_ART': 'O'
}

IsAcharyaLabelLoaded = False

if os.path.exists('NEREntities.json'):
    with open('NEREntities.json') as f:
        AcharyaLabels = json.load(f)
        IsAcharyaLabelLoaded = True

def convert2AcharyaLabel(conllLabel):
    if IsAcharyaLabelLoaded:
        if conllLabel in AcharyaLabels['EntityMap']:
            return AcharyaLabels['EntityMap'][conllLabel]['key']
    return conllLabel

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

    #Converting from conll evaluation data to plain txt
    def getWord(line):
        lineData = line.split()
        if len(lineData) > 0:
            return lineData[0]
        return line

    evalRecord = " ".join(map(getWord, evalData.split("\n")))
    logging.info(logPrefix + "Received record for evaluation %s with len: %d", evalData, len(evalData))

    doc = ner(evalRecord)
    logging.info(logPrefix + "processing ner..")

    output = []
    for tok in doc:
        label = tok.ent_iob_
        if label != "O":
            ent = "O"
            if tok.ent_type_ in ModelLabelsToCONLL:
                ent = convert2AcharyaLabel(ModelLabelsToCONLL[tok.ent_type_])
            if ent != "O":
                label += '-' + ent 
            else:
                label = "O"
        output.append("\t".join([str(tok), label]))

    logging.info(output)
    conn.sendall("\n".join(output).encode("utf-8"))

    logging.info(logPrefix + "Sent output done with the record")
    conn.close()


