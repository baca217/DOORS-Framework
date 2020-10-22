import json

def return_sentence(rec_info):
    sentences = ""
    for i in rec_info:
        y = json.loads(i)
        sentences = sentences + " " +y["text"]
    return sentences
