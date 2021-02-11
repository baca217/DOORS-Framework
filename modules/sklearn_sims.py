import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
#from nltk.corpus import stopwords
#import Levenshtein #testing


#def clean_string(text): #removes words that might be uncessary for overall structure of the sentence
    #still needs some adjusment
#    text = ''.join([word for word in text if word not in string.punctuation])
#    text = text.lower()
#    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
#    return text

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
    #print("------NORMAL-------")

    bScore = 0 #keeping track of the best score for cosine comparison
    bComm = "" #best sentence matched
    bOrig = "" #representation of best sentence

    for i in range(len(comTypes)):
        if comTypes[i].strip() == "exact":
            #print("exact matching")
            #print("sentence 1: ", commands[i][0])
            #print("sentence 2: ", spoken)
            if commands[i][0] in spoken: #exact matches will return immediately
                    return commands[i][0]
        if comTypes[i].strip() == "cosine":
            tempArr = commands[i] #pulling similar commands
            tempArr.append(spoken) #adding spoken command to vectorize it
            vectorizer = CountVectorizer().fit_transform(tempArr) #vectorize
            vectors = vectorizer.toarray() #turn to array
            for j in range(len(tempArr)-1):
                ret = cosine_sim_vectors(vectors[-1], vectors[j]) #compare spoken vector to command vector
                #print("sentence 1: ", tempArr[-1])
                #print("sentence 2: ", tempArr[j])
                #print("similarity: ", ret)
                #print("distance:",Levenshtein.distance(spoken, tempArr[j]),"\n")
                if ret > .8 and ret > bScore:
                    bScore = ret
                    bComm = tempArr[j]
                    bOrig = tempArr[0]
    #print("Best score:",bScore,"\nBest match:",bComm)
    return bOrig


def compare_command(spoken):
    c_file = open("/home/pi/Documents/DOORS/modules/commands.txt", "r")
    commands = c_file.read()
    commands = commands.split("\n")
    commands = [x for x in commands if x != ""] #removing empty entries
    classify = []
    for x in range(len(commands)): #pulling classification type from word
        temp = commands[x].split(",")[-1] #classification is always at the end
        commands[x] = commands[x].replace(temp, "").strip() #remove classification type
        classify.append(temp)
    arrCommands = []
    for i in commands:
        arrCommands.append(list(filter(None, i.split(",")))) #splitting command variations, removing empty strings
    if "hey homie" in spoken:
        spoken = spoken.replace("hey homie ", "").strip()
    elif "homie" in spoken:
        spoken = spoken.replace("homie ",  "").strip()
    elif "hey homey" in spoken:
        spoken = spoken.replace("hey homey ", "").strip()
    elif "homey" in spoken:
        spoken = spoken.replace("homey ",  "").strip()

    else:
        print("homie was not detected!")
        return -1, -1

    result = comp_work(spoken, arrCommands, classify)
    #clean_comp_work(spoken, arrCommands, classify)
    #print("result:",result)

    return spoken, result
