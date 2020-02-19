import random
import pyfiglet
import sys
import time

class WordPhrase:
    def __init__(self, fr_word, fr_phrase, en_word, en_phrase):
        self.fr_word = fr_word
        self.fr_phrase = fr_phrase
        self.en_word = en_word
        self.en_phrase = en_phrase

def write_slow(text_line):
    for char in text_line:
        time.sleep(0.08)
        sys.stdout.flush()
        sys.stdout.write(char)


### ------ SETUP DATA

fr1 = open('vocabData/fr_words.txt', 'r')
fr2 = open('vocabData/fr_phrases.txt', 'r')
en1 = open('vocabData/en_words.txt', 'r')
en2 = open('vocabData/en_phrases.txt', 'r')
fr_words = fr1.readlines()
fr_phrases = fr2.readlines()
en_words = en1.readlines()
en_phrases = en2.readlines()

instance_fr_w = []
instance_fr_ph = []
instance_en_w = []
instance_en_ph = []
for fr_w, fr_ph, en_w, en_ph in zip(fr_words, fr_phrases, en_words, en_phrases):
    instance_fr_w.append(fr_w.strip('\n').lower())
    instance_fr_ph.append(fr_ph.strip('\n').lower())
    instance_en_w.append(en_w.strip('\n').lower())
    instance_en_ph.append(en_ph.strip('\n').lower()+' [...]')

# Create dictionary to store all WordPhrase objects
allWordPhrases = {fr_word: WordPhrase(fr_word, fr_phrase, en_word, en_phrase) for fr_word, fr_phrase, en_word, en_phrase in zip(instance_fr_w, instance_fr_ph, instance_en_w, instance_en_ph)}

fr1.close()
fr2.close()
en1.close()
en2.close()


### ------ BEGIN GAME

# Greet player and give instructions
welcome_banner = pyfiglet.figlet_format("Quiz Time!")
print(welcome_banner)
print("You will be shown French words and to gain points you have to type the correct English translation.\n")
print("If you get stuck, type 'clue svp' to be shown the French word used in a phrase.\n")
print("If you can't get it, just type 'next word' and you'll be shown the answer and given a new word.\n")
print("If you want to quit and see your score, type 'au revoir.'\n")
input("Let's go! Press enter to begin!\n")

score = 0
total_words = 0
right_first_time = 0
guess_count = 0
win_banner = pyfiglet.figlet_format('Bravo!')
new_word = True

for guess in range(0, 10000000):

    if (new_word):
        # Randomly choose from dictionary of WordPhrases to play the game!
        total_words += 1
        randChoice = random.choice(list(allWordPhrases.keys()))
        current_word = allWordPhrases[randChoice].fr_word
        print('---> '+str(current_word))
    en_guess = input("Your guess: ")
    guess_count += 1
    if (en_guess == allWordPhrases[randChoice].en_word):
        score += 1
        if (guess_count == 1):
            right_first_time +=1
        print(win_banner)
        guess_count = 0
        new_word = True
        print('Next word:')
        continue

    elif (en_guess == 'clue svp'):
        print(allWordPhrases[randChoice].fr_phrase)
        guess_count =- 1 # Input was not a guess
        new_word = False
        continue

    elif (en_guess == 'next word'):
        print('The answer was:')
        print(allWordPhrases[randChoice].en_word)
        print(allWordPhrases[randChoice].en_phrase)
        guess_count = 0
        print('')
        print('New word:')
        new_word = True
        continue

    elif (en_guess == 'au revoir'):
        print('')
        print('Thanks for playing!')
        first_time_percent = int((float(right_first_time)/ float(score))*100)
        print('You got '+str(score)+'/'+str(total_words)+' right and '+str(first_time_percent)+'% right first time!')
        break

    else:
        print('Pas exactement. Try again!')
        new_word = False
        continue
