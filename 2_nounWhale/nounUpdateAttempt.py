# Ideas:
## Initialise lists of spriteLists of male and female nouns (as in verbDrop)
## Check for collisions with each (and +/-1 score), remove only noun collided with
## After certain time interval if possible??: pop(0) from male and female list of lists, then randomly swap between drawing the male or female list


'''
TODO/ issues:
- Create separate lists for male and female nouns, then as separate sprite lists
- Add condition to gain point for masculin noun and lose for feminin nouns
- Update noun creation loop so that word changes
- Look for better French text formatting
- Add different collision sound for gain or lose points

Adapted from Arcade examples:
- https://realpython.com/arcade-python-game-framework/
- https://arcade.academy/examples/sprite_collect_coins_move_down.html#sprite-collect-coins-move-down

Stock images:
- https://www.pngfuel.com/free-png/vindr

'''

import random
import numpy as np
from PIL import Image, ImageDraw
import arcade
import pyfiglet


### --------------- SETUP OBJECTS FOR FRENCH WORDS -----------------------------------

class frenchNoun:
    def __init__(self, fr_word, en_word):
        self.fr_word = fr_word
        self.en_word = en_word



f_list = open('vocabData/f_nouns+defArticle.txt', 'r')
f_nouns = f_list.readlines()
m_list = open('vocabData/m_nouns+defArticle.txt', 'r')
m_nouns = m_list.readlines()

female_fr = []
female_en = []
male_fr = []
male_en = []
for line in f_nouns:
    female_fr.append(line.split()[1])
    female_en.append(line.split()[2])
for line in m_nouns:
    male_fr.append(line.split()[1])
    male_en.append(line.split()[2])

# Create dictionary to store all noun objects
maleNouns = {fr_word: frenchNoun(fr_word, en_word) for fr_word, en_word in zip(male_fr, male_en)}
femaleNouns = {fr_word: frenchNoun(fr_word, en_word) for fr_word, en_word in zip(female_fr, female_en)}

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
noun_count = 10
rounds = 20

male_en_list =[] 
male_fr_list = []
female_en_list =[] 
female_fr_list = []
win_banner = pyfiglet.figlet_format('vous gagnez !')
lose_banner = pyfiglet.figlet_format("c'est dommage !")
fini_banner = pyfiglet.figlet_format("c'est fini !")



def setupNouns(self, maleNouns, femaleNouns, male_en_list, male_fr_list, female_en_list, female_fr_list): 
    # Set up lists to contain lists of different sprites (initial length = rounds) 

    # Male nouns 
    for j in range(rounds):
        # Randomly select verb
        randChoice = random.choice(list(maleNouns.keys()))
        current_word = maleNouns[randChoice]
        # Single static en noun drawn at top of screen
        translation = current_word.en_word.encode('utf-8')
        img2 = Image.new('RGB', (80, 20), color = (0, 191, 255))
        d2 = ImageDraw.Draw(img2)
        d2.text((10,5), translation, fill=(255,255,0))
        img2.save('images/male_noun_en_'+str(j)+'.png')
        male_en = Coin('images/male_noun_en_'+str(j)+'.png', SCALING) 
        male_en.center_x = 658 
        male_en.center_y = 1160
        male_en_list.append(male_en)
        # Create the mobile fr nouns
        img = Image.new('RGB', (80, 20), color = (248, 131, 121))
        d = ImageDraw.Draw(img)
        word = current_word.fr_word.encode('utf-8')
        d.text((10,5), word, fill=(255,255,0))
        img.save('images/male_noun_fr_'+str(j)+'.png')
        noun = Coin('images/male_noun_fr_'+str(j)+'.png', SCALING)
        # Add male fr noun to the list of sprite lists
        male_fr_spriteList = arcade.SpriteList()
        for i in range(noun_count):
            # Position the nouns
            noun.center_x = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH+500)
            noun.center_y = random.randrange(SCREEN_HEIGHT)
            male_fr_spriteList.append(noun)
        male_fr_list.append(male_fr_spriteList)

    # Female nouns 
    for j in range(rounds):
        # Randomly select verb
        randChoice = random.choice(list(femaleNouns.keys()))
        current_word = femaleNouns[randChoice]
        # Single static en noun drawn at top of screen
        translation = current_word.en_word.encode('utf-8')
        img2 = Image.new('RGB', (80, 20), color = (0, 191, 255))
        d2 = ImageDraw.Draw(img2)
        d2.text((10,5), translation, fill=(255,255,0))
        img2.save('images/female_noun_en_'+str(j)+'.png')
        female_en = Coin('images/female_noun_en_'+str(j)+'.png', SCALING) 
        female_en.center_x = 658 
        female_en.center_y = 1160
        female_en_list.append(female_en)
        # Create the mobile fr nouns
        img = Image.new('RGB', (80, 20), color = (248, 131, 121))
        d = ImageDraw.Draw(img)
        word = current_word.fr_word.encode('utf-8')
        d.text((10,5), word, fill=(255,255,0))
        img.save('images/female_noun_fr_'+str(j)+'.png')
        noun = Coin('images/female_noun_fr_'+str(j)+'.png', SCALING)
        # Add female fr noun to the list of sprite lists
        female_fr_spriteList = arcade.SpriteList()
        for i in range(noun_count):
            # Position the nouns
            noun.center_x = random.randrange(SCREEN_WIDTH, SCREEN_WIDTH+500)
            noun.center_y = random.randrange(SCREEN_HEIGHT)
            female_fr_spriteList.append(noun)
        female_fr_list.append(female_fr_spriteList)




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
        self.center_y = random.randrange(SCREEN_HEIGHT)
        self.center_x = random.randrange(SCREEN_WIDTH + 100, SCREEN_WIDTH + 700)
    def update(self):
        # Move the noun
        self.center_x -= 0.2
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
        #self.player_sprite = None
        self.all_sprites = arcade.SpriteList()
        self.noun_sprite_list = arcade.SpriteList()
        self.noun_en_sprite_list = arcade.SpriteList()
        self.current_gender = 'male'


    def setup(self):
        """Get the game ready to play
        """
        # Set the background color
        arcade.set_background_color(arcade.color.CATALINA_BLUE)
        # Setup the player
        self.player = arcade.Sprite("images/whale.png", SCALING*0.25)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)

        setupNouns(self, maleNouns, femaleNouns, male_en_list, male_fr_list, female_en_list, female_fr_list)

        chance = random.randrange(100)
        if chance%2 == 0:
            print('male')
            self.current_gender = 'male'
        else:
            print('female')
            self.current_gender = 'female'


        # Spawn a new plastic waste every 3 seconds
        arcade.schedule(self.add_plastic, 3.0)

        # Load our background music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        #self.background_music = arcade.load_sound(
        #    "sounds/Apoxode_-_Electric_1.wav"
        #)

        # Load our other sounds
        # Sound sources: Jon Fincher
        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.move_up_sound = arcade.load_sound("sounds/Rising_putter.wav")
        self.move_down_sound = arcade.load_sound("sounds/Falling_putter.wav")
        # Start the background music
        #arcade.play_sound(self.background_music)

        # Unpause everything and reset the collision timer
        self.paused = False
        self.collided = False
        self.collision_timer = 0.0

    
    def change_nouns(self, delta_time: float):
        # Remove top noun from all lists
        male_en_list.pop(0)
        male_fr_list.pop(0)
        female_en_list.pop(0)
        female_fr_list.pop(0)
        # Randomly chose male or female list for next noun
        chance = random.randrange(100)
        if chance%2 == 0:
            print('male')
            self.current_gender = 'male'
        else:
            print('female')
            self.current_gender = 'female'


    def add_plastic(self, delta_time: float):
        """Adds a new cloud to the screen
        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """
        # First, create the new cloud sprite
        bottle = FlyingSprite("images/plastic_bottle2.png", SCALING*0.1)
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

        if self.current_gender == 'male':
            # Generate a list of all male nouns that collided with the player, gain a point
            hit_list_male = arcade.check_for_collision_with_list(self.player, male_fr_list[0])
            # Loop through each colliding sprite, remove it, and add to the score.
            for noun in hit_list_male:
                noun.remove_from_sprite_lists()
                self.score += 1
                if len(male_fr_list) == 0:
                    print(win_banner)
                    print('')
                    print('You scored '+str(self.score)+' out of a possible '+str(rounds)+'.\n')
                    arcade.close_window()
        if self.current_gender == 'female':
            # Generate a list of all female nouns that collided with the player, lose a point
            hit_list_female = arcade.check_for_collision_with_list(self.player, female_fr_list[0])
            # Loop through each colliding sprite, remove it, and add to the score.
            for noun in hit_list_female:
                noun.remove_from_sprite_lists()
                self.score -= 1
                if len(female_fr_list) == 0:
                    print(lose_banner)
                    print('')
                    print('You scored '+str(self.score)+' out of a possible '+str(rounds)+'.\n')
                    arcade.close_window()


        # Move fr nouns
        if self.current_gender == 'female':
            female_fr_list[0].update()
        if self.current_gender == 'male':
            male_fr_list[0].update()

        # Schedule to change nouns every 10 seconds
        arcade.schedule(self.change_nouns, 10.0)


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
        #self.noun_sprite_list.draw()
        #self.noun_en_sprite_list.draw()
        if self.current_gender == 'female':
            female_en_list[0].draw()
            female_fr_list[0].draw()
        if self.current_gender == 'male':
            male_en_list[0].draw()
            male_fr_list[0].draw()

        # Write score and translation of current_word to bottom left corner of screen
        arcade.draw_text("Mange tous les nouns masculins!", 20, 1150, arcade.color.RED, 28)
        #translation = f"{self.current_word.fr_word} = {self.current_word.en_word}"
        #arcade.draw_text(translation, 20, 1100, arcade.color.BLACK, 28)
        write_score = f"Score: {self.score}"
        arcade.draw_text(write_score, 10, 400, arcade.color.RED, 28)
        # Add seaweed to background
        texture = arcade.load_texture("images/seaweed.png")
        seaweed_loc = [300.0, 500.0, 600.0, 900.0, 1250.0, 1300.0, 1400.0]
        for x in seaweed_loc:
            arcade.draw_texture_rectangle(x, 600.0, 200.0, 400.0, texture, 0, 155)




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
            print(fini_banner)
            print('')
            print('You scored '+str(self.score)+' out of a possible '+str(rounds)+'.\n')
            arcade.close_window()
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