import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import modules.module_loader as ml
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
            if commands[i][0] in spoken: #exact matches will return immediately
                    return commands[i][0], -1
        if comTypes[i].strip() == "cosine":
            tempArr = commands[i] #pulling similar commands
            tempArr.append(spoken) #adding spoken command to vectorize it
            vectorizer = CountVectorizer().fit_transform(tempArr) #vectorize
            vectors = vectorizer.toarray() #turn to array
            for j in range(len(tempArr)-1):
                ret = cosine_sim_vectors(vectors[-1], vectors[j]) #compare spoken vector to command vector
                if ret > .8 and ret > bScore:
                    bScore = ret
                    bComm = tempArr[j]
                    bOrig = tempArr[0]
    return bOrig, bScore

def check_homie(sentence):
    '''
    The code below is for checking if some variation of "hey homie" occurred within the recording
    This should be taken care of by the front end but I wil leave it here just in case
    '''

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



'''
FUNCTION: compare_command
ARGUMENTS: spoke
DESCRIPTION: functions takes one argument which is "spoken" which is a string. This string will be
compared to all the commands for the known modules.
'''
def compare_command(spoken):
    mods = ml.modules() #dictionary containing modules for usage
    bScore = 0
    bSent = ""
    bMod = ""
    for i in mods.keys(): #iterating through module names
        commands, classify = mods[i].commands()
        result, score = comp_work(spoken, commands, classify)
        if score == -1: #exact match was found
            mods[i].command_handler(spoken)
            bScore = -1
            break
        if score > bScore and score > .8: #new best score
            bScore = score
            bSent = result
            bMod = i
    if bScore > .8:
        mods[bMod].comman_handler(spoken)
        print("result: "+bSent)
    return spoken, result
