import random
import numpy as np

class frenchVerb:
    def __init__(self, fr_verb, en_verb):
        self.fr_verb = fr_verb
        self.en_verb = en_verb

    def get_hint(self):
        # Prints half of the characters in the string, randomly selected
        letters = range(0, len(self.fr_verb))
        hint_indices = random.sample(letters,len(self.fr_verb)/2)
        hint = []
        for letter in letters:
            if letter in hint_indices:
                hint += self.fr_verb[letter]
            else:
                hint += '?'
        print(hint)  



### SETUP OBJECTS

verb_list = open('verbs_sorted.txt', 'r')
all_verbs = verb_list.readlines()

fr_verbs = []
en_verbs = []
for line in all_verbs: 
    fr_verbs.append(line.split()[0])
    en_verbs.append(line.split()[1]+' '+line.split()[2])

# Create dictionary to store all WordPhrase objects
verbObjects = {fr_verb: frenchVerb(fr_verb, en_verb) for fr_verb, en_verb in zip(fr_verbs, en_verbs)}

verb_list.close()

# Randomly select verb
randChoice = random.choice(list(verbObjects.keys()))
current_word = verbObjects[randChoice].en_verb

print("Here's your verb: "+str(current_word))


def get_hint(word):
    # Prints half of the characters in the string, randomly selected
    letters = range(0, len(word))
    hint_indices = random.sample(letters,len(word)/2)
    hint = []
    for letter in letters:
        if letter in hint_indices:
            hint += word[letter]
        else:
            hint += '?'
    print(hint)


print(verbObjects[randChoice].fr_verb)

print(get_hint(verbObjects[randChoice].fr_verb))

#print("Here's your hint: "+get_hint(verbObjects[randChoice].get_hint()))