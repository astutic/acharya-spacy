
import os
import json

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

