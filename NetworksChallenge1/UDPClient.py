from socket import *
from utils import *
import pickle
import re

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
            newWords.append("__" + words[i-1] + "__" + words[i] + "_?")
        else:
            newWords.append("%_" + words[i-1] + "_&" + words[i] + "&_" + words[i+1] + "_%")
    return pickle.dumps(newWords)


##### Define your processing protocol for responses here!
def parseResponse(responseList):
    words = pickle.loads(responseList)
    rList = []
    match = ""
    fList = []
    for word in words:
        #print(word) # uncomment to see what you are receiving as a response
        if re.findall("^\^.*", word):#first word
            match = re.findall("^\^.*", word)
            print("start: ", match)
            rList.append(match)
        elif re.findall("^__.*_\?$", word):
            match = re.findall("^__.*_\?$", word)
            print("end: ", match)
            rList.append(match)
        elif re.findall("^%_.*_%$", word):
            match = re.findall("^%_.*_%$", word)
            print("middle: ", match)
            rList.append(match)
   #for item in rlist:
   #    sum = 2+2

    





    sentence = ' '.join(words)
    print(rList)
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
#print(response)
demoAccuracy(messages[0], response) # Testing one sentence from the demo


# TESTING BLOCK (Once you are done with your checking algorithm)
# set done to True once you're ready!
done = False
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
