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

def compare_command(commands):
    #words that don't mean anything overall, may be removed, needs adjusting
    #stopwords = stopwords.words('english')

    c_len = len(commands)
    c_file = open("commands.txt", "r")
    sentences = c_file.read()
    sentences = sentences.split("\n")
    sentences = commands + [x for x in sentences if x != ""]

    #algorithm needs some adjusment
    #cleaned = list(map(clean_string, sentences))
    #print(cleaned)

    vectorizer = CountVectorizer().fit_transform(sentences)
    vectors = vectorizer.toarray()
    print(vectors)

    for y in range (c_len): 
        print("--------------------------------------")
        for x in range (c_len, len(sentences)):
            ret = cosine_sim_vectors(vectors[y], vectors[x])
            print("sentence 1: ",sentences[y])
            print("sentence 2: ",sentences[x])
            print("similarity: ",ret,"\n")
