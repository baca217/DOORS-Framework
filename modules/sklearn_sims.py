import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import Levenshtein #testing


def clean_string(text): #removes words that might be uncessary for overall structure of the sentence
    #still needs some adjusment
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
    return text

def cosine_sim_vectors(vec1, vec2): #comparison of two sentences
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]

def clean_comp_work(spoken, commands, comTypes):
    print("------CLEAN-------")
    commands.append(spoken) #append spoken for vectorization
    oldCommands = commands.copy()

    #algorithm needs some adjusment
    cleaned = list(map(clean_string, commands))
    spoken = cleaned[-1]
    commands = cleaned
    #print(cleaned)

    vectorizer = CountVectorizer().fit_transform(commands)
    vectors = vectorizer.toarray()
    bScore = 0 #keeping track of the best score for cosine comparison
    bComm = ""

    for i in range(len(comTypes)):
        if comTypes[i] == "exact":
            if commands[i] in spoken: #exact matches will return immediately
                    return oldCommands[i]
        if comTypes[i] == "cosine":
                ret = cosine_sim_vectors(vectors[-1], vectors[i]) #compare spoken vector to command vector
                print("sentence 1: ", commands[-1])
                print("sentence 2: ", commands[i])
                print("similarity: ", ret)
                print("distance:",Levenshtein.distance(spoken, commands[i]),"\n")
                if ret > .8 and ret > bScore:
                    bScore = ret
                    bComm = oldCommands[i]
    return bComm


def comp_work(spoken, commands, comTypes):
    commands.append(spoken) #append spoken for vectorization
    print("------NORMAL-------")
    #algorithm needs some adjusment
    cleaned = list(map(clean_string, commands))
    #print(cleaned)

    vectorizer = CountVectorizer().fit_transform(commands)
    vectors = vectorizer.toarray()
    bScore = 0 #keeping track of the best score for cosine comparison
    bComm = ""

    for i in range(len(comTypes)):
        if comTypes[i] == "exact":
            if commands[i] in spoken: #exact matches will return immediately
                    return commands[i]
        if comTypes[i] == "cosine":
                ret = cosine_sim_vectors(vectors[-1], vectors[i]) #compare spoken vector to command vector
                print("sentence 1: ", commands[-1])
                print("sentence 2: ", commands[i])
                print("similarity: ", ret)
                print("distance:",Levenshtein.distance(spoken, commands[i]),"\n")
                if ret > .8 and ret > bScore:
                    bScore = ret
                    bComm = commands[i]
    return bComm


def compare_command(spoken):
    c_file = open("/home/pi/Documents/DOORS/modules/commands.txt", "r")
    commands = c_file.read()
    commands = commands.split("\n")
    commands = [x for x in commands if x != ""]
    classify = []
    for x in range(len(commands)): #pulling classification from word
        temp = commands[x].split()[-1]
        commands[x] = commands[x].replace(temp, "").strip()
        classify.append(temp)
    print("commands: ",commands)
    print("classify: ",classify)

    if "homie" in spoken:
        spoken = spoken.replace("homie ",  "")
    else:
        print("homie was not detected! Exiting....")
        exit()

    result = comp_work(spoken, commands, classify)
    clean_comp_work(spoken, commands, classify)
    print("result:",result)

    return spoken, result
