"""
Sprite move between different rooms.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_rooms
"""

import arcade
import os
from pyfirmata import Arduino, util
import time
import serial

"""Arduino
SDA -> A4, SCL -> A5"""
ser = serial.Serial('/dev/cu.usbmodem1411')

class ArduinoData:
    """
    This class holds all the input from the arduino
    """
    def __init__(self):
        self.acc = ["x", "y", "z"]
        self.gyr = ["x", "y", "z"]


def set_Arduino_data():
    arduino = ArduinoData()

    for x in range(6):
        arduinoData = ser.readline().decode("utf-8").strip('\n').strip('\r')
        try:
            arduinoData = int(arduinoData)

        except ValueError:
            arduinoData = 0

        if (x < 3):
            arduino.acc[x] = arduinoData
        else:
            arduino.gyr[x-3] = arduinoData
    return arduino

"""The GAME"""
SPRITE_SCALING = 0.2
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Sprite Rooms Example"

MOVEMENT_SPEED = 5


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

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("images/brick.jpg", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up on the right side
            if x == 0:
                wall = arcade.Sprite("images/brick.jpg", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)



    # If you want coins or monsters in a level, then add that code here.
    """wall = arcade.Sprite("images/brick.jpg", 1)
    wall.left = 500 # * SPRITE_SIZE
    wall.bottom = 320 #  * SPRITE_SIZE
    room.wall_list.append(wall)"""

    # Load the background image for this level.
    room.background = arcade.load_texture("images/background.jpg")

    return room


def setup_room_2():
    """
    Create and return room 2.
    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # -- Set up the walls
    # Create bottom and top row of boxes
    # This y loops a list of two, the coordinate 0, and just under the top of window
    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        # Loop for each box going across
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("images/brick.jpg", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    # Create left and right column of boxes
    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        # Loop for each box going across
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            # Skip making a block 4 and 5 blocks up
            if x != 0:
                wall = arcade.Sprite("images/brick.jpg", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite("images/brick.jpg", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture("images/background2.jpg")

    return room


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

        # Sprite lists
        self.current_room = 0

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
        self.player_sprite = arcade.Sprite("images/stick.png", SPRITE_SCALING)
        self.player_sprite.center_x = 600
        self.player_sprite.center_y = 119
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Our list of rooms
        self.rooms = []

        # Create the rooms. Extend the pattern for each room.
        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
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

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_acc_change(self):
        self.arduino_data = set_Arduino_data()
        print("x:")
        print(self.arduino_data.acc[0])
        print("y:")
        print(self.arduino_data.acc[1])
        print("z:")
        print(self.arduino_data.acc[2])

        """Fixed movement - not done
        top_value = 10000
        low_value = -10000


        #y-axis -16000 to 16000
        if self.arduino_data.acc[1] > 14000:
            self.player_sprite.change_y = MOVEMENT_SPEED
        if 10000 < self.arduino_data.acc[1] < 14000:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if 0 < self.arduino_data.acc[1] < 10000:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = MOVEMENT_SPEED
        if -10000 < self.arduino_data.acc[1] < 0:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = -MOVEMENT_SPEED
        if -10000 < self.arduino_data.acc[1] < -14000:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.arduino_data.acc[1] < -14000:
            self.player_sprite.change_y = MOVEMENT_SPEED
        """

        """Free movement"""
        top_value = 2000
        low_value = -2000
        # x-axis
        if self.arduino_data.acc[0] < low_value:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.arduino_data.acc[0] > top_value:
            self.player_sprite.change_x = MOVEMENT_SPEED

        #y-axis
        if self.arduino_data.acc[1] < low_value:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif self.arduino_data.acc[1] > top_value:
            self.player_sprite.change_y = MOVEMENT_SPEED

        # Stand still
        if self.arduino_data.acc[0] > low_value and self.arduino_data.acc[0] < top_value:
            self.player_sprite.change_x = 0
        if self.arduino_data.acc[1] > low_value and self.arduino_data.acc[1] < top_value:
            self.player_sprite.change_y = 0

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()
        self.on_acc_change()

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
