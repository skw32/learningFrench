'''
TODO/ issues:
- Update verbs
- Issue with formatting of French words (improved but not solved by utf8)

Adapted from Arcade examples:
- https://realpython.com/arcade-python-game-framework/
- https://arcade.academy/examples/sprite_collect_coins_move_down.html#sprite-collect-coins-move-down

French vocab source:
- http://ekladata.com/6FxXu86fl5mQwo7lEyDS5hG9NTc.pdf

'''

import random
import numpy as np
from PIL import Image, ImageDraw
import arcade
import re


### --------------- SETUP OBJECTS FOR FRENCH WORDS -----------------------------------

class frenchVerb:
    def __init__(self, fr_verb, en_verb):
        self.fr_verb = fr_verb
        self.en_verb = en_verb


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


### -------------------- BEGIN GAME ----------------------------------


# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "VERB DROP"
SCALING = 2.0
verb_count = 10

# Randomly select verb
randChoice = random.choice(list(verbObjects.keys()))
current_word = verbObjects[randChoice]


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
    (Modified to represent words in the present game)
    """
    def reset_pos(self):
        # Reset the words to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT+200, SCREEN_HEIGHT+800)
        self.center_x = random.randrange(SCREEN_WIDTH)
    def update(self):
        # Move the word down
        self.center_y -= 1
        # See if the word has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
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
        self.score = score
        #self.player_sprite = None
        self.all_sprites = arcade.SpriteList()
        self.verb_sprite_list = arcade.SpriteList()
        self.verb_fr_sprite_list = arcade.SpriteList()
        self.wrong_verb_sprite_list = arcade.SpriteList()



    def setup(self):
        """Get the game ready to play
        """
        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)
        # Setup the player
        self.player = arcade.Sprite("images/bucket.png", SCALING*0.25)
        self.player.center_y = SCREEN_HEIGHT-200
        self.player.left = SCREEN_WIDTH / 2
        self.all_sprites.append(self.player)

        # Create the noun instance !!CURRENT BUG WITH FRENCH WORDS WITH ACCENTS!!
        # Single static fr verb
        img2 = Image.new('RGB', (80, 20), color = (255, 255, 255))
        d2 = ImageDraw.Draw(img2)
        translation = current_word.fr_verb.encode('utf-8')
        d2.text((10,5), translation, fill=(0,0,0))
        img2.save('images/verb_fr.png')
        verb_fr = Coin("images/verb_fr.png", SCALING) 
        verb_fr.center_x = 140 
        verb_fr.center_y = 1080
        self.verb_fr_sprite_list.append(verb_fr)
        
        # Create the mobile en verbs (correct match)
        for i in range(verb_count):
            img = Image.new('RGB', (90, 20), color = (49, 140, 231))
            d = ImageDraw.Draw(img)
            word = current_word.en_verb.encode('utf-8')
            d.text((10,5), word, fill=(0,0,0))
            img.save('images/verb.png')
            verb = Coin("images/verb.png", SCALING)
            # Position the verbs
            verb.center_x = random.randrange(SCREEN_WIDTH+1500)
            verb.center_y = random.randrange(SCREEN_HEIGHT+500)
            # Add the fr verb to the list
            self.verb_sprite_list.append(verb)

        # Create the mobile en verbs (wrong verbs)
        for i in range(verb_count):
            # Generate new random verb and check that it is not the same as the right verb
            randChoice = random.choice(list(verbObjects.keys()))
            wrong_word = verbObjects[randChoice]
            while wrong_word == current_word:
                randChoice = random.choice(list(verbObjects.keys()))
                wrong_word = verbObjects[randChoice]
            img = Image.new('RGB', (90, 20), color = (49, 140, 231))
            d = ImageDraw.Draw(img)
            word = wrong_word.en_verb.encode('utf-8')
            d.text((10,5), word, fill=(0,0,0))
            img.save('images/wrong_verb.png')
            verb = Coin("images/wrong_verb.png", SCALING)
            # Position the verbs
            verb.center_x = random.randrange(SCREEN_WIDTH+1500)
            verb.center_y = random.randrange(SCREEN_HEIGHT+500)
            # Add the fr verb to the list
            self.wrong_verb_sprite_list.append(verb)

        # Load our other sounds
        # Sound sources: Jon Fincher
    #    self.collision_sound = arcade.load_sound("sounds/Collision.wav")
    #    self.move_up_sound = arcade.load_sound("sounds/Rising_putter.wav")
    #    self.move_down_sound = arcade.load_sound("sounds/Falling_putter.wav")
        # Start the background music
        #arcade.play_sound(self.background_music)

        # Unpause everything and reset the collision timer
        self.paused = False
        self.collided = False
        self.collision_timer = 0.0



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



        # Generate a list of all right verbs that collided with the player, gain a point
        win_list = arcade.check_for_collision_with_list(self.player, self.verb_sprite_list)
        # Loop through each colliding sprite, remove it, and add to the score.
        for verb in win_list:
            verb.remove_from_sprite_lists()
            self.score += 1
        # Generate a list of all wrong verbs that collided with the player, lose a point
        lose_list = arcade.check_for_collision_with_list(self.player, self.wrong_verb_sprite_list)
        # Loop through each colliding sprite, remove it, and add to the score.
        for verb in lose_list:
            verb.remove_from_sprite_lists()
            self.score -= 1

        # Move fr verbs
        self.verb_sprite_list.update()
        self.wrong_verb_sprite_list.update()


        # Update everything
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time
            )
            #sprite.center_y = int(
            #    sprite.center_y + sprite.change_y * delta_time
            #)
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
        self.wrong_verb_sprite_list.draw()
        self.verb_sprite_list.draw()
                
        # Add clouds and rainbow to background
        cloud = arcade.load_texture("images/cloud.png")
        rainbow = arcade.load_texture("images/rainbow.png")
        arcade.draw_texture_rectangle(150.0, 1080.0, 300.0, 250.0, cloud, 0, 255)
        arcade.draw_texture_rectangle(700.0, 1060.0, 900.0, 300.0, rainbow, 0, 255)
        arcade.draw_texture_rectangle(1300.0, 1080.0, 300.0, 250.0, cloud, 0, 255)
        # Put after to ensure on top of clouds
        self.verb_fr_sprite_list.draw() 
        arcade.draw_text("Attrape le verb:", 55, 1110, arcade.color.BLACK, 20)
        write_score = f"Score: {self.score}"
        arcade.draw_text(write_score, 1225, 1070, arcade.color.RED, 28)
        



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

        #if symbol == arcade.key.I or symbol == arcade.key.UP:
        #    self.player.change_y = 250
        #    arcade.play_sound(self.move_up_sound)

        #if symbol == arcade.key.K or symbol == arcade.key.DOWN:
        #    self.player.change_y = -250
        #    arcade.play_sound(self.move_down_sound)


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
        '''
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.K
            or symbol == arcade.key.UP
            or symbol == arcade.key.DOWN
        ):
            self.player.change_y = 0
        '''
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