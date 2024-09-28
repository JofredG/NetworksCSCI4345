from socket import *
from utils import *
import pickle
import re, math

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

##### Define your preparation protocol here!
def prepMsg(sentence):
    words = sentence.split() # splits the sentence into words
    newWords = []
    for i in range(len(words)):
        if i == 0:
            newWords.append("^_" + words[i] + "__" + words[i+1])
        elif i == len(words)-1:
            newWords.append("__" + words[i-1] + "_?" + words[i] + "_?")
        else:
            newWords.append("%_" + words[i-1] + "_&" + words[i] + "&_" + words[i+1] + "_%")
    return pickle.dumps(newWords)


##### Define your processing protocol for responses here!
def parseResponse(responseList):
    words = pickle.loads(responseList)
    rList = []
    match = ""
    for word in words:
        #print(word) # uncomment to see what you are receiving as a response
        if re.findall("^\^.*", word):#first word
            match = re.findall("\^_(\w+)__",word) #using regex we get the first word of the sentence
            #print("start: ", match)
            match = ' '.join(match) #turns the list containing a single string(match) into just string
            rList.insert(0, match) #insert first word at first index
            words.pop(words.index(word)) #remove first word from list of words
        elif re.findall("^_?.*_\?$", word):
            match = re.findall("_?(\w+.)_\?$", word)
            #print("end: ", match)
            match = ' '.join(match)
            rList.append(match)
            words.pop(words.index(word)) #remove last word from words
    #print("words: ", words)
    #print("rList w start and end: ", rList)
    for word in words:
            currentWord = re.findall("_&(\w+)&_", word)
            middle_word_1 = re.findall("^%_(\w+)_&", word) #prev word #regex return a list of items matching declared pattern
            middle_word_2 = re.findall("&_(\w+)_%$", word) #next word
            currentWord = ' '.join(currentWord)
            prevWord = ' '.join(middle_word_1) #convert from list item to string
            nextWord = ' '.join(middle_word_2)
            
            #print("currentWord: ", currentWord) # Debug print
            #print("middle_word_1:", prevWord)  # Debug print
            #print("middle_word_2:", nextWord)  # Debug print
            #print("rList:", rList)  # Debug print
            
            if prevWord in rList:
                rList.insert(rList.index(prevWord)+1, currentWord)
                #print("it works and we've entered")
            elif nextWord in rList:
                rList.insert(rList.index(nextWord), currentWord)
                #print("it works and we've entered")
            else:
                rList.insert(math.ceil(len(rList)/2), currentWord)

    #print("rList: ", rList)
    sentence = ' '.join(rList)
    return sentence

# Load a message from your text file
messages = []
with open('demoMessages.txt', 'r') as f:
    for sentence in f.readlines():
        messages.append(sentence)

message = prepMsg(messages[0]) # Grabs the first message in the demo file, you can change this (0-4)
# message = input('input lowercase: sentence:') # Use this for your own test sentence

clientSocket.sendto(message, (serverName, serverPort))
response, serverAddress = clientSocket.recvfrom(2048)
response = parseResponse(response)
print(response)
demoAccuracy(messages[0], response) # Testing one sentence from the demo


# TESTING BLOCK (Once you are done with your checking algorithm)
# set done to True once you're ready!
done = True
if done:
    tests = []
    total = 0
    with open('testMessages.txt', 'r') as f:
        for sentence in f.readlines():
            clientSocket.sendto(prepMsg(sentence), (serverName, serverPort))
            response, _ = clientSocket.recvfrom(2048)
            response = parseResponse(response)
            total += testAccuracy(sentence, response)
        print(f'Your test score is: {total}%!')

clientSocket.close()
