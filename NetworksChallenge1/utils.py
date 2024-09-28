import pickle
import random

def demoAccuracy(original, modified):
    try:
        original = original.lower().split()
        modified = modified.lower().split()
        score = 100*sum([original[i] == modified[i] for i in range(len(original))]) / len(original)
    except:
        score = 0

    print(f'Your demo score is: {score}%!')


def testAccuracy(original, modified):
    try:
        original = original.lower().split()
        modified = modified.lower().split()
        return sum([original[i] == modified[i] for i in range(len(original))]) / len(original)
    except:
        return 0

def garble(message):
    # Messages will arrive in the wrong order
    wordList = pickle.loads(message)
    random.shuffle(wordList)

    # They may also have corrupted data!
    for i in range(len(wordList)):
        if random.randint(0, 99) < 5:
            wordList[i] = '!@#$'
    return pickle.dumps(wordList)