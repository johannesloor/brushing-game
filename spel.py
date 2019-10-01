import arcade
import os
import time
import random
#import arduino


SPRITE_SCALING = 0.1
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

DIRT_COUNT = 500
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "BRUSHI"

MOVEMENT_SPEED = 15
TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1

class Room:
    """
    This class holds all the information about the
    different rooms.
    """
    def __init__(self):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wall_list = None

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None


def setup_room_1():
    """
    Create and return room 1.
    If your program gets large, you may want to separate this into different
    files.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # If you want coins or monsters in a level, then add that code here.
    """wall = arcade.Sprite("images/brick.jpg", 1)
    wall.left = 450 # * SPRITE_SIZE
    wall.bottom = 320 #  * SPRITE_SIZE
    room.wall_list.append(wall)"""

    # Load the background image for this level.
    room.background = arcade.load_texture("images/bglevel1.png")

    return room

class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.
        texture = arcade.load_texture("images/fairy.png", mirrored=True, scale=SPRITE_SCALING)
        self.textures.append(texture)
        texture = arcade.load_texture("images/fairy.png", scale=SPRITE_SCALING)
        self.textures.append(texture)

        # By default, face right.
        self.set_texture(TEXTURE_RIGHT)

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0

        # Sprite lists
        self.current_room = 0
        self.dirt_list = None

        # Set up the player
        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

        # Set up arduino data
        self.arduino_data = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.player_sprite = Player()
        self.player_sprite.center_x = 600
        self.player_sprite.center_y = 119
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        #Set up dirts
        self.dirt_list = arcade.SpriteList()
        # Create the dirts
        for i in range(DIRT_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            dirt = arcade.Sprite("images/stick.png", SPRITE_SCALING)

            # Position the coin
            dirt.center_x = random.randrange(450, 550)
            dirt.center_y = random.randrange(350, SCREEN_HEIGHT-30)

            # Add the coin to the lists
            self.dirt_list.append(dirt)
        # Our list of rooms
        self.rooms = []

        # Create the rooms. Extend the pattern for each room.
        room = setup_room_1()
        self.rooms.append(room)

        # Our starting room number
        self.current_room = 0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)

        # Draw all the walls in this room
        self.rooms[self.current_room].wall_list.draw()

        # If you have coins or monsters, then copy and modify the line
        # above for each list.

        self.player_list.draw()
        self.dirt_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN:
            self.player_sprite.center_x = SCREEN_WIDTH/2
            self.player_sprite.center_y = 180
            #self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.center_x = 300
            self.player_sprite.center_y = SCREEN_HEIGHT*0.7
            self.player_sprite.set_texture(TEXTURE_LEFT)
            #self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.center_x = 1000
            self.player_sprite.center_y = SCREEN_HEIGHT*0.7
            self.player_sprite.set_texture(TEXTURE_RIGHT)
            #self.player_sprite.change_x = MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def add_to_timer(self):
        self.frame_count += 1
        print(self.frame_count)

    def remove_dirt(self):
        if self.frame_count == 1200//DIRT_COUNT and self.dirt_list: #About 30sek
            self.dirt_list[0].kill()
            self.frame_count = 0

    def on_acc_change(self):
        self.arduino_data = arduino.set_Arduino_data()
        x_gyr = self.arduino_data.gyr[0]
        y_gyr = self.arduino_data.gyr[1]
        z_gyr = self.arduino_data.gyr[2]

        x_acc = self.arduino_data.acc[0]
        y_acc = self.arduino_data.acc[1]
        z_acc = self.arduino_data.acc[2]
        #print("x:")
        #print(x_gyr)
        #print("y:")
        #print(y_gyr)
        #print("z:")
        #print(z_gyr)

        """Fixed movement"""


        #y-axis -16000 to 16000
        if y_gyr > 9000:
            self.player_sprite.center_x = 300
            self.player_sprite.center_y = SCREEN_HEIGHT*0.7
            self.player_sprite.set_texture(TEXTURE_LEFT)
        elif -9000 < y_gyr < 9000:
            self.player_sprite.center_x = SCREEN_WIDTH/2
            self.player_sprite.center_y = 180
        elif y_gyr < -9000:
            self.player_sprite.center_x = 1000
            self.player_sprite.center_y = SCREEN_HEIGHT*0.7
            self.player_sprite.set_texture(TEXTURE_RIGHT)



        """Free movement
        top_value = 2000
        low_value = -2000
        # x-axis
        if x_gyr < low_value:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif x_gyr > top_value:
            self.player_sprite.change_x = MOVEMENT_SPEED

        #y-axis
        if y_gyr < low_value:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif y_gyr > top_value:
            self.player_sprite.change_y = -MOVEMENT_SPEED

        # Stand still
        if low_value < x_gyr < top_value:
            self.player_sprite.change_x = 0
        if low_value < y_gyr < top_value:
            self.player_sprite.change_y = 0
        """
    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()
        #self.on_acc_change()
        if self.player_sprite.center_x == 300:
            self.add_to_timer()
            self.remove_dirt()
        # Do some logic here to figure out what room we are in, and if we need to go
        # to a different room.
        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
