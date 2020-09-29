import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords


def clean_string(text): #removes words that might be uncessary for overall structure of the sentence
    #still needs some adjusment
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

def cosine_sim_vectors(vec1, vec2): #comparison of two sentences
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]

#words that don't mean anything overall
stopwords = stopwords.words('english')

sentences = [
        'Homie turn on the lights',
        'Homie the lights must be turned on',
        'Homie can you turn on the lights please',
        'Homie the lights on they must be'
        ]

#algorithm needs some adjusment
#cleaned = list(map(clean_string, sentences))
#print(cleaned)

vectorizer = CountVectorizer().fit_transform(sentences)
vectors = vectorizer.toarray()
print(vectors)
v1 = 0
v2 = 0
while 1:
    v1 = int(input("Number for v1: "))
    v2 = int(input("Number for v2: "))
    if v1 is -1 or v2 is -1:
        break
    ret = cosine_sim_vectors(vectors[v1], vectors[v2])
    print("sentence 1: ",sentences[v1])
    print("sentence 2: ",sentences[v2])
    print("similarity: ",ret)
