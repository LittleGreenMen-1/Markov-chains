import random
import pickle
from datetime import datetime

chain = {}

def load_chain():
    global chain

    try:
        with open("markov_chain.txt", 'rb') as file:
            chain = pickle.load(file)
    except Exception as e:
        print(e)
        chain = {}

def save_chain():
    global chain

    with open("markov_chain.txt", 'wb') as file:
        pickle.dump(chain, file)

def train(username):
    global chain

    username = "[" + username + "]"

    for i in range(0, len(username) - 1):
        letter = username[i]
        next_letter = username[i + 1]

        if chain.get(letter) == None:
            freq_dict = {}
        else:
            freq_dict = chain[letter]

        if freq_dict.get(next_letter) == None:
            freq_dict.update([(next_letter, 0)])

        value = freq_dict[next_letter]
        freq_dict.update([(next_letter, value + 1)])

        chain.update([(letter, freq_dict)])

if __name__ == "__main__":
    random.seed(datetime.now())

    load_chain()

    username = ""
    character = '['

    while character != ']':
        username += character

        total = 0
        for letter in chain[character]:
            total += chain[character][letter]

        lucky_number = random.randint(0, total)

        for letter in chain[character]:
            lucky_number -= chain[character][letter]
            if lucky_number <= 0:
                character = letter
                break

    username = username[1:]

    print(username)

    # chain = {}
    # usernames = []
    #
    # with open("Markov/usernames.txt", 'r') as usrn:
    #     for line in usrn.readlines():
    #         usernames.append(line[:-1].lower())
    #
    # for username in usernames:
    #     train(username)
    #
    # save_chain()