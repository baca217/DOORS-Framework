import json

def return_sentences(rec_info):
    sentences = []
    for i in rec_info:
        y = json.loads(i)
        sentences.append(y["text"])
    return sentences
