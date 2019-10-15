import random
import pickle
from datetime import datetime

chain = {}

def load_chain():
    global chain

    try:
        with open("trained.txt", 'rb') as file:
            chain = pickle.load(file)
    except Exception as e:
        print(e)
        chain = {}

def save_chain():
    global chain

    with open("trained.txt", 'wb') as file:
        pickle.dump(chain, file)

def train(sentence):
    global chain

    words = sentence.split(' ')
    words.insert(0, "[")
    words.append("]")

    l = len(words) - 1
    i = 0

    while i < l:
        if len(words[i]) == 1:
            i += 1
            pass

        if words[i][-1:] == '?' or words[i][-1:] == '!' or words[i][-1:] == '.' or words[i][-1:] == ',':
            words.insert(i + 1, words[i][-1:])
            words[i] = words[i][:-1]
            l += 1
        i += 1

    for i in range(0, len(words) - 1):
        word = words[i]
        next_word = words[i + 1]

        if chain.get(word) == None:
            freq_dict = {}
        else:
            freq_dict = chain[word]

        if freq_dict.get(next_word) == None:
            freq_dict.update([(next_word, 0)])

        value = freq_dict[next_word]
        freq_dict.update([(next_word, value + 1)])

        chain.update([(word, freq_dict)])

def build_chain():
    global chain

    chain = {}
    sentences = []

    with open("tex.t", 'r') as lines:
        for line in lines.readlines():
            sentences.append(line[:-1])

    for sentence in sentences:
        train(sentence)

    save_chain()

def build_sentence():
    sentence = ""
    word = "["

    while word != "]":
        sentence += word + " "

        total = 0
        for w in chain[word]:
            total += chain[word][w]

        lucky_number = random.randint(0, total)

        for w in chain[word]:
            lucky_number -= chain[word][w]
            if lucky_number <= 0:
                word = w
                break

    return sentence[2:]

if __name__ == "__main__":
    random.seed(datetime.now())

    loaded = False
    choice = '1'

    while choice == '1' or choice == '2':
        choice = input("1. Build the chain\n2. Build a sentence\n")

        if choice != '1' and choice != '2':
            print("Invalid choice")
            break

        if choice == '1':
            build_chain()

        if choice == '2':
            if not loaded:
                load_chain()
                loaded = True

            s = build_sentence()
            print(s)
