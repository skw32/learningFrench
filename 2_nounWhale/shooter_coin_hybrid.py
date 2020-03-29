'''
TODO/ issues:
- Translation corresponds to last iteration of noun list, doesn't match flying sprite
- Update noun creation loop so that word changes
- Create 'le', 'la' and 'l' whales with condition to lose or gain points for bad or good match
- Modify images of words and look for better French text formatting
- Re-draw whale, change background colour, sounds


Adapted from Arcade examples:
- https://realpython.com/arcade-python-game-framework/
- https://arcade.academy/examples/sprite_collect_coins_move_down.html#sprite-collect-coins-move-down

Stock images:
- https://www.pngfuel.com/free-png/vindr

French vocab source:
- http://ekladata.com/6FxXu86fl5mQwo7lEyDS5hG9NTc.pdf

'''

import random
import numpy as np
from PIL import Image, ImageDraw
import arcade


### --------------- SETUP OBJECTS FOR FRENCH WORDS -----------------------------------

class frenchNoun:
    def __init__(self, gender, fr_word, def_art, en_word):
        self.gender = gender
        self.fr_word = fr_word
        self.en_word = en_word
        self.def_art = def_art

        if (gender =='f'):
            self.indef_art = 'une'
        elif (gender == 'm'):
            self.indef_art = 'un'
        else:
            self.indef = 'error'


f_list = open('vocabData/f_nouns+defArticle.txt', 'r')
f_nouns = f_list.readlines()
m_list = open('vocabData/m_nouns+defArticle.txt', 'r')
m_nouns = m_list.readlines()

genders = []
def_arts = []
fr_words = []
en_words = []
for line in f_nouns:
    genders.append('f')
    def_arts.append(line.split()[0])
    fr_words.append(line.split()[1])
    en_words.append(line.split()[2])
for line in m_nouns:
    genders.append('m')
    def_arts.append(line.split()[0])
    fr_words.append(line.split()[1])
    en_words.append(line.split()[2])

# Create dictionary to store all noun objects
nounObjects = {en_word: frenchNoun(gender, fr_word, def_art, en_word) for gender, fr_word, def_art, en_word in zip(genders, fr_words, def_arts, en_words)}

f_list.close()
m_list.close()

'''
randChoice = random.choice(list(nounObjects.keys()))
current_word = nounObjects[randChoice]
print(current_word.fr_word)
print(current_word.def_art)
print(current_word.gender)
print(current_word.en_word)
print(current_word.indef_art)
'''


### -------------------- BEGIN GAME ----------------------------------


# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "NOUN WHALE"
SCALING = 2.0
noun_count = 20


class FlyingSprite(arcade.Sprite):
    """Base class for all flying sprites
    Flying sprites include enemies and clouds
    """
    def update(self):
        """Update the position of the sprite
        When it moves off screen to the left, remove it
        """
        # Move the sprite
        super().update()
        # Remove us if we're off screen
        if self.right < 0:
            self.remove_from_sprite_lists()



class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    (Modified to represent nouns in the present game)
    """
    def reset_pos(self):
        # Reset the noun to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT+500)
        self.center_x = random.randrange(SCREEN_WIDTH + 700, SCREEN_WIDTH+1500)
    def update(self):
        # Move the noun
        self.center_x -= 1
        # See if the noun has fallen off the bottom of the screen.
        # If so, reset it.
        if self.right < 0:
            self.reset_pos()



class SpaceShooter(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title, score):
        """Initialize the game
        """
        super().__init__(width, height, title)
        # Setup the empty sprite lists
        self.plastic_list = arcade.SpriteList()
        self.score = score
        self.noun_list = None
        #self.player_sprite = None
        self.all_sprites = arcade.SpriteList()
        self.noun_sprite_list = arcade.SpriteList()

    def setup(self):
        """Get the game ready to play
        """
        # Set the background color
        arcade.set_background_color(arcade.color.PINK)
        # Setup the player
        self.player = arcade.Sprite("images/whale.png", SCALING*0.25)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        # Create the nouns
        for i in range(noun_count):
            # Create the noun instance !!CURRENT BUG WITH FRENCH WORDS WITH ACCENTS!!
            # Randomly select noun
            randChoice = random.choice(list(nounObjects.keys()))
            self.current_word = nounObjects[randChoice]

            img = Image.new('RGB', (100, 25), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            word = self.current_word.fr_word.encode('utf8')
            d.text((10,10), word, fill=(255,255,0))
            img.save('images/noun.png')
            noun = Coin("images/noun.png", SCALING)
            # Position the coin
            noun.center_x = random.randrange(SCREEN_WIDTH+1500)
            noun.center_y = random.randrange(SCREEN_HEIGHT+500)
            # Add the coin to the lists
            self.noun_sprite_list.append(noun)



        # Spawn a new plastic waste every 3 seconds
        arcade.schedule(self.add_plastic, 3.0)

        # Load our background music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        self.background_music = arcade.load_sound(
            "sounds/Apoxode_-_Electric_1.wav"
        )
        # Load our other sounds
        # Sound sources: Jon Fincher
        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.move_up_sound = arcade.load_sound("sounds/Rising_putter.wav")
        self.move_down_sound = arcade.load_sound("sounds/Falling_putter.wav")
        # Start the background music
        arcade.play_sound(self.background_music)

        # Unpause everything and reset the collision timer
        self.paused = False
        self.collided = False
        self.collision_timer = 0.0


    def add_plastic(self, delta_time: float):
        """Adds a new cloud to the screen
        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        # First, create the new cloud sprite
        bottle = FlyingSprite("images/bottle_test.png", SCALING*0.1)
        # Set its position to a random height and off screen right
        bottle.left = random.randint(self.width, self.width + 10)
        bottle.top = random.randint(10, self.height - 10)
        # Set its speed to a random speed heading left
        bottle.velocity = (random.randint(-50, -20), 0)
        # Add it to the enemies list
        self.plastic_list.append(bottle)
        self.all_sprites.append(bottle)



    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If we're paused, do nothing
        Once everything has moved, check for collisions between
        the player and the list of enemies

        Arguments:
            delta_time {float} -- Time since the last update
        """
        # If we're paused, don't update anything
        if self.paused:
            return


        # Generate a list of all plastic waste that collided with the player, lose 10 points
        hit_list_plastic = arcade.check_for_collision_with_list(self.player, self.plastic_list)
        # Loop through each colliding sprite, remove it, and add to the score.
        for bottle in hit_list_plastic:
            bottle.remove_from_sprite_lists()
            self.score -= 10

        # Generate a list of all nouns that collided with the player, gain a point
        hit_list = arcade.check_for_collision_with_list(self.player, self.noun_sprite_list)
        # Loop through each colliding sprite, remove it, and add to the score.
        for noun in hit_list:
            noun.remove_from_sprite_lists()
            self.score += 1


        # Move nouns
        self.noun_sprite_list.update()

        # Update everything
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )
        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0



    def on_draw(self):
        """Draw all game objects
        """
        arcade.start_render()
        self.all_sprites.draw()
        self.noun_sprite_list.draw()
        # Write score and translation of current_word to bottom left corner of screen
        write_score = f"Score: {self.score}"
        arcade.draw_text(write_score, 10, 400, arcade.color.RED, 28)
        translation = f"{self.current_word.fr_word} = {self.current_word.en_word}"
        arcade.draw_text(translation, 10, 450, arcade.color.BLACK, 22)




    # ---------------------- All keyboard controls ---------------------------

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause the game
        I/J/K/L: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.I or symbol == arcade.key.UP:
            self.player.change_y = 250
            arcade.play_sound(self.move_up_sound)

        if symbol == arcade.key.K or symbol == arcade.key.DOWN:
            self.player.change_y = -250
            arcade.play_sound(self.move_down_sound)

        if symbol == arcade.key.J or symbol == arcade.key.LEFT:
            self.player.change_x = -250

        if symbol == arcade.key.L or symbol == arcade.key.RIGHT:
            self.player.change_x = 250
    def on_key_release(self, symbol: int, modifiers: int):
        """Undo movement vectors when movement keys are released

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            symbol == arcade.key.J
            or symbol == arcade.key.L
            or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = 0




if __name__ == "__main__":
    # Create a new Space Shooter window
    space_game = SpaceShooter(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE, 0)
    # Setup to play
    space_game.setup()
    # Run the game
    arcade.run()