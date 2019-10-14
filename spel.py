import arcade
import os
import time
import random

use_arduino = False
if use_arduino:
    import arduino

SPRITE_SCALING = 0.1
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

DIRT_COUNT = 50
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "BRUSHI"

MOVEMENT_SPEED = 20
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


def setup_level(dirt, background, cord_left, cord_center, cord_right):
    """
    Create and return room 1.
    If your program gets large, you may want to separate this into different
    files.

    Input:
    dirt: path to dirt image
    background: path to background image
    cord_left, cord_center and cord right: list of cordinates in the form
    [x-width, x-height, y-width, y-height]

    """
    room = Room()

    """ Set up the game and initialize the variables. """
    # Sprite lists
    room.wall_list = arcade.SpriteList()

    # If you want coins or monsters in a level, then add that code here.
    #Set up dirts
    room.dirt_left_list = arcade.SpriteList()
    room.dirt_center_list = arcade.SpriteList()
    room.dirt_right_list = arcade.SpriteList()

    # Create the dirts
    for i in range(DIRT_COUNT):

        # Create the coin instance
        # Coin image from kenney.nl
        dirt_left = arcade.Sprite(dirt, SPRITE_SCALING)
        dirt_center_list = arcade.Sprite(dirt, SPRITE_SCALING)
        dirt_right_list = arcade.Sprite(dirt, SPRITE_SCALING)

        # Position the coin
        dirt_left.center_x = random.randrange(cord_left[0], cord_left[1])
        dirt_left.center_y = random.randrange(cord_left[2], cord_left[3])

        dirt_center_list.center_x = random.randrange(cord_center[0], cord_center[1])
        dirt_center_list.center_y = random.randrange(cord_center[2], cord_center[3])

        dirt_right_list.center_x = random.randrange(cord_right[0], cord_right[1])
        dirt_right_list.center_y = random.randrange(cord_right[2], cord_right[3])

        # Add the coin to the lists
        room.dirt_left_list.append(dirt_left)
        room.dirt_center_list.append(dirt_center_list)
        room.dirt_right_list.append(dirt_right_list)
    # Load the background image for this level.
    room.background = arcade.load_texture(background)

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
        self.dirt_left_list = None
        self.dirt_center_list = None
        self.dirt_right_list = None

        #Timer
        self.left_timer = 0
        self.center_timer = 0
        self.right_timer = 0
        self.total_time = 0.0

        # Set up the player
        self.rooms = None
        self.player = None
        self.player_list = None
        self.physics_engine = None
        self.position_center_x = 550
        self.position_center_y = 160
        self.position_left_x = 200
        self.position_right_x = 900
        self.position_lr_y = SCREEN_HEIGHT*0.7

        # Set up arduino data
        self.arduino_data = None
        self.acc_Y_list = []
        self.acc_X_list = []
        self.acc_Z_list = []

        self.start_game = False
        self.shake_value = 0
        self.shake_value_list = [0]

        self.view_bottom = 0
        self.view_left = 0

        #Animation
        self.frame_timer = 0
        self.texture_choice = 1


    def setup(self):
        """ Set up the game and initialize the variables. """
        # Set up the player
        self.player_list = arcade.SpriteList()
        #self.player = Player()


        # Our list of rooms
        self.rooms = []

        self.player = arcade.Sprite()
        self.player.append_texture(arcade.load_texture("images/animation1-14.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation2-14.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation3-14.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation4-14.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation3-14.png", mirrored=True, scale=SPRITE_SCALING))

        self.player.append_texture(arcade.load_texture("images/animation1-14.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation2-14.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation3-14.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation4-14.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/animation3-14.png", scale=SPRITE_SCALING))
        self.player.center_x = self.position_center_x
        self.player.center_y = self.position_center_y
        self.player.set_texture(0)
        self.player_list.append(self.player)



        # Create the rooms. Extend the pattern for each room.
        room = setup_level("images/apple.png","images/bglevel1.png",
        cord_left=[350, 480, 400, SCREEN_HEIGHT-20],
        cord_center=[370, 730, 300, 400],
        cord_right=[620, 770, 400, SCREEN_HEIGHT-20])
        self.rooms.append(room)

        room = setup_level("images/stick.png","images/bglevel3.png",
        cord_left=[350, 480, 400, SCREEN_HEIGHT-20],
        cord_center=[370, 730, 300, 400],
        cord_right=[620, 770, 400, SCREEN_HEIGHT-20])
        self.rooms.append(room)

        room = setup_level("images/pinapple.png","images/bglevel4.png",
        cord_left=[350, 480, 400, SCREEN_HEIGHT-20],
        cord_center=[370, 730, 300, 400],
        cord_right=[620, 770, 400, SCREEN_HEIGHT-20])
        self.rooms.append(room)

        room = setup_level("images/apple.png","images/bglevel2.png",
        cord_left=[350, 480, 400, SCREEN_HEIGHT-20],
        cord_center=[370, 730, 300, 400],
        cord_right=[620, 770, 400, SCREEN_HEIGHT-20])
        self.rooms.append(room)

        # Our starting room number
        self.current_room = 0

        # Create a physics engine for this room
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.rooms[self.current_room].wall_list)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)

        #self.player_list[self.texture_choice].draw()
        self.player.draw()
        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(output, 50, SCREEN_HEIGHT-50, arcade.color.BLACK, 30)


        # Draw dirt
        left_dirt = self.rooms[self.current_room].dirt_left_list
        right_dirt = self.rooms[self.current_room].dirt_right_list
        center_dirt = self.rooms[self.current_room].dirt_center_list

        left_dirt.draw()
        right_dirt.draw()
        center_dirt.draw()

        # Draw player



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.SPACE:
            if self.start_game:
                self.start_game = False
            else:
                self.start_game = True

        if self.start_game:
            if key == arcade.key.UP:
                self.reset_timer('left')
                self.reset_timer('right')
                self.reset_timer('center')

                if self.current_room == 0:
                    self.current_room = 1
                else:
                    self.current_room = 0
            if key == arcade.key.DOWN:
                self.player.center_x = self.position_center_x
                self.player.center_y = self.position_center_y
                #self.player.change_y = -MOVEMENT_SPEED
            if key == arcade.key.LEFT:
                self.player.center_x = self.position_left_x
                self.player.center_y = self.position_lr_y
                self.texture_choice = 1

                #self.player.change_x = -MOVEMENT_SPEED
            if key == arcade.key.RIGHT:
                self.player.center_x = self.position_right_x
                self.player.center_y = self.position_lr_y
                self.texture_choice = 6

            self.player.set_texture(self.texture_choice)


                #self.player.change_x = MOVEMENT_SPEED


    def add_to_timer(self, direction):
        if direction == "left":
            self.left_timer += 1
        elif direction == "center":
            self.center_timer += 1
        elif direction == "right":
            self.right_timer += 1

    def reset_timer(self, direction):
        if direction == "left":
            self.left_timer = 0
        elif direction == "center":
            self.center_timer = 0
        elif direction == "right":
            self.right_timer = 0

    def remove_dirt(self, direction):
        self.add_to_timer(direction)
        remove_dirt_frame = 160//DIRT_COUNT #About 10s total
        timers = [self.left_timer, self.center_timer, self.right_timer]
        lists = [self.rooms[self.current_room].dirt_left_list, self.rooms[self.current_room].dirt_center_list, self.rooms[self.current_room].dirt_right_list]
        for x in range(len(timers)):
            if lists[x]:
                if timers[x] == remove_dirt_frame:
                    self.reset_timer(direction)
                    lists[x][0].kill()

    def get_avg(self, list):
        total = 0
        for y in list:
            total += y
        avg = total//len(list)
        return avg

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
        if not self.acc_Y_list:
            self.acc_Y_list.append(y_acc)
        else:
            self.acc_Y_list.insert(0, y_acc)
            if len(self.acc_Y_list) > 20:
                self.acc_Y_list.pop(-1)
        acc_Y_avg = self.get_avg(self.acc_Y_list)

        if not self.acc_X_list:
            self.acc_X_list.append(x_acc)
        else:
            self.acc_X_list.insert(0, x_acc)
            if len(self.acc_X_list) > 20:
                self.acc_X_list.pop(-1)
        acc_X_avg = self.get_avg(self.acc_X_list)

        if not self.acc_Z_list:
            self.acc_Z_list.append(z_acc)
        else:
            self.acc_Z_list.insert(0, z_acc)
            if len(self.acc_Z_list) > 20:
                self.acc_Z_list.pop(-1)
        acc_Z_avg = self.get_avg(self.acc_Z_list)
        """
        print('x:')
        print(acc_X_avg)
        print()
        print('z:')
        print(acc_Z_avg)
        print()
        print('y:')
        print(acc_Y_avg)
        """
        shake = (x_gyr + y_gyr + z_gyr)//3
        self.shake_value_list.insert(0, shake)
        if len(self.shake_value_list) > 20:
            self.shake_value_list.pop(-1)

        self.shake_value = self.get_avg(self.shake_value_list)

        """Fixed movement"""
        #y-axis -16000 to 16000
        if acc_Y_avg > 10000:
            self.player.center_x = self.position_left_x
            self.player.center_y = self.position_lr_y
            self.texture_choice = 1
        elif -5000 < acc_Y_avg < 5000:
            self.player.center_x = self.position_center_x
            self.player.center_y = self.position_center_y
        elif acc_Y_avg < -10000:
            self.player.center_x = self.position_right_x
            self.player.center_y = self.position_lr_y
            self.texture_choice = 6

        self.player.set_texture(self.texture_choice)

    def animate_player(self):
        animation_framerate = 6
        animation_list = [0, animation_framerate, animation_framerate * 2, animation_framerate * 3]
        for frame in animation_list:
            if self.frame_timer == frame:
                self.player.set_texture(self.texture_choice + self.frame_timer//animation_framerate)

        max_timer = animation_list[-1] + animation_framerate
        if self.frame_timer < max_timer/2:
            self.player.change_y = 1
        else:
            self.player.change_y = -1
        self.frame_timer += 1
        if self.frame_timer == max_timer:
            self.frame_timer = 0


    def switch_level(self, next_level, speed):
        left_dirt = self.rooms[self.current_room].dirt_left_list
        right_dirt = self.rooms[self.current_room].dirt_right_list
        center_dirt = self.rooms[self.current_room].dirt_center_list

        if not left_dirt and not right_dirt and not center_dirt:
            self.start_game = False
            self.player.set_texture(0)
            self.reset_timer('left')
            self.reset_timer('right')
            self.reset_timer('center')
            self.player.change_y = speed

            if self.player.center_y < - 150 or self.player.center_y > SCREEN_HEIGHT + 150:
                self.player.change_y = -speed
                self.current_room = next_level
                self.player.center_x = self.position_center_x

    def check_if_change_level(self):
        if self.current_room == 0:
            self.switch_level(1, 10)

        elif self.current_room == 1:

            if not self.start_game and self.player.center_y < self.position_center_y:
                self.player.change_y = 0
                self.start_game = True
            else:
                self.switch_level(2, 10)

        elif self.current_room == 2:
            center_y = self.position_center_y
            lr_y = self.position_lr_y
            self.position_center_y = lr_y
            self.position_lr_y = center_y
            if not self.start_game and self.player.center_y < self.position_center_y:
                self.player.change_y = 0
                self.start_game = True
            else:
                self.switch_level(3, -10)

        elif self.current_room == 3:
            if not self.start_game and self.player.center_y > self.position_center_y:
                self.player.change_y = 0
                self.start_game = True
            else:
                self.switch_level(4, -10)


    def update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()
        self.check_if_change_level()


        if self.start_game:
            self.total_time += delta_time

            #self.player_list.update()
            if use_arduino:
                self.on_acc_change()
            if not 150 < self.shake_value < 450:
                self.animate_player()
                if self.player.center_x == self.position_left_x:
                    self.remove_dirt('left')
                elif self.player.center_x == self.position_right_x:
                    self.remove_dirt('right')
                else:
                    self.remove_dirt('center')
            else:
                self.player.set_texture(0)
                if self.player.center_x == self.position_right_x:
                    self.player.set_texture(5)



def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
