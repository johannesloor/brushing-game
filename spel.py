import arcade
import os
import time
import random
import statistics
import pygame

use_arduino = False
if use_arduino:
    import arduino

test_mode = False

SPRITE_SCALING = 0.1
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

DIRT_COUNT = 1 #30
DIRT_SCALING = 0.45
SCREEN_WIDTH = 2638*0.45 #1200
SCREEN_HEIGHT = 1664*0.45#700
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


def setup_level(dirt_left, dirt_center, dirt_right, background, dirt_count, dirt_scaling, cord_left, cord_center, cord_right):
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
    if dirt_count:
        for i in range(dirt_count):

            # Create the coin instance
            dirt_left = arcade.Sprite(dirt_left, dirt_scaling)
            dirt_center_list = arcade.Sprite(dirt_center, dirt_scaling)
            dirt_right_list = arcade.Sprite(dirt_right, dirt_scaling)

            # Position the dirt
            dirt_left.center_x = cord_left[0]
            dirt_left.center_y = cord_left[1]

            dirt_center_list.center_x = cord_center[0]
            dirt_center_list.center_y = cord_center[1]

            dirt_right_list.center_x = cord_right[0]
            dirt_right_list.center_y = cord_right[1]

            """dirt_left.center_x = random.randrange(cord_left[0], cord_left[1])
            dirt_left.center_y = random.randrange(cord_left[2], cord_left[3])

            dirt_center_list.center_x = random.randrange(cord_center[0], cord_center[1])
            dirt_center_list.center_y = random.randrange(cord_center[2], cord_center[3])

            dirt_right_list.center_x = random.randrange(cord_right[0], cord_right[1])
            dirt_right_list.center_y = random.randrange(cord_right[2], cord_right[3])"""

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
        self.dirt_left_list = None
        self.dirt_center_list = None
        self.dirt_right_list = None

        #Levels
        self.current_room = 0
        self.start_screen = 0
        self.intro1 = 1
        self.intro2 = 2
        self.intro3 = 3
        self.intro4 = 4
        self.intro5 = 5
        self.level1 = 6
        self.level2 = 7
        self.level3 = 8
        self.level4 = 9
        self.done = 10


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
        self.position_center_x = 600
        self.position_center_y = 120
        self.position_left_x = 280
        self.position_right_x = 950
        self.position_lr_y = 460

        # Set up arduino data
        self.arduino_data = None
        self.acc_Y_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        self.acc_X_list = []
        self.acc_Z_list = []
        self.force = 0
        self.shake_value = 0
        self.shake_value_list = []

        self.start_game = False
        self.start_intro = False
        self.playing_song = False

        self.view_bottom = 0
        self.view_left = 0

        #Animation
        self.frame_timer = 0
        self.texture_choice = 15
        self.test = 0
        self.paus_level = True
        self.glitter_count = 0


    def setup(self):
        """ Set up the game and initialize the variables. """
        #Set music
        pygame.mixer.init(44100, -16,2,2048)
        pygame.mixer.music.load("Funky_Space_Princess.wav")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()

        # Set up the player
        self.player_list = arcade.SpriteList()
        #self.player = Player()

        self.player = arcade.Sprite()
        #Facing Right
        self.player.append_texture(arcade.load_texture("images/player/left/0.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/1.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/2.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/3.png", mirrored=True, scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/2.png", mirrored=True, scale=SPRITE_SCALING))

        #Facin left
        self.player.append_texture(arcade.load_texture("images/player/left/0.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/1.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/2.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/3.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/left/2.png", scale=SPRITE_SCALING))

        #Up
        self.player.append_texture(arcade.load_texture("images/player/down/down0.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/down/down1.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/down/down2.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/down/down3.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/down/down2.png", scale=SPRITE_SCALING))

        #Down
        self.player.append_texture(arcade.load_texture("images/player/up/up0.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/up/up1.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/up/up2.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/up/up3.png", scale=SPRITE_SCALING))
        self.player.append_texture(arcade.load_texture("images/player/up/up2.png", scale=SPRITE_SCALING))
        self.player.center_x = self.position_center_x
        self.player.center_y = self.position_center_y
        self.player.set_texture(15)
        self.player_list.append(self.player)

        # Our list of rooms
        self.rooms = []

        #Start page
        room = setup_level("","","","images/background/start-screen.png",0,1,
        cord_left = 0,
        cord_center = 0,
        cord_right = 0)
        room.logo = arcade.Sprite("images/logo-1.png", 0.2)
        room.logo.center_x = SCREEN_WIDTH/2
        room.logo.center_y = SCREEN_HEIGHT-130#/2 +100
        self.rooms.append(room)

        #Intro
        room = setup_level("","","","images/background/dirty-mouth.png",0,1,
        cord_left = 0,
        cord_center = 0,
        cord_right = 0)
        self.rooms.append(room)

        room = setup_level("","","","images/background/levels.png",0,1,
        cord_left = 0,
        cord_center = 0,
        cord_right = 0)
        self.rooms.append(room)

        room = setup_level("","","","images/background/levels.png",0,1,
        cord_left = 0,
        cord_center = 0,
        cord_right = 0)
        self.rooms.append(room)

        room = setup_level("","","","images/background/levels.png",0,1,
        cord_left = 0,
        cord_center = 0,
        cord_right = 0)
        self.rooms.append(room)

        room = setup_level("","","","images/background/levels.png",0,1,
        cord_left = 0,
        cord_center = 0,
        cord_right = 0)
        self.rooms.append(room)

        # Create the rooms. Extend the pattern for each room.
        room = setup_level("images/dirt/level1/blåslime1.png","images/dirt/level1/rosaslime1.png","images/dirt/level1/grönslime1.png","images/background/level1.png",DIRT_COUNT,0.45,
        cord_left=[589, 373],
        cord_center=[590, 373],
        cord_right=[592, 373])
        self.rooms.append(room)

        room = setup_level("images/dirt/hamburgare.png","images/dirt/hamburgare.png","images/dirt/hamburgare.png","images/background/level2.png",DIRT_COUNT,0.08,
        cord_left=[480, 220],
        cord_center=[770, 465],
        cord_right=[880, 300])
        self.rooms.append(room)

        room = setup_level("images/dirt/cupcake.png","images/dirt/cupcake.png","images/dirt/cupcake.png","images/background/level3.png",DIRT_COUNT,0.1,
        cord_left=[320, 320],
        cord_center=[450, 503],
        cord_right=[680, 270])
        self.rooms.append(room)

        room = setup_level("images/dirt/apple.png","images/dirt/apple.png","images/dirt/apple.png","images/background/level4.png",DIRT_COUNT,0.1,
        cord_left=[350, 320],
        cord_center=[550, 300],
        cord_right=[730, 500])
        self.rooms.append(room)

        room = setup_level("","","","images/background/clean-mouth.png",0,1,
        cord_left = 0,
        cord_center = 0,
        cord_right = 0)
        self.rooms.append(room)

        self.glitter = arcade.Sprite()
        self.glitter.append_texture(arcade.load_texture("images/glitter/glitter1.png", scale=0.6))
        self.glitter.append_texture(arcade.load_texture("images/glitter/glitter2.png", scale=0.6))
        self.glitter.center_x = SCREEN_WIDTH/2
        self.glitter.center_y = SCREEN_HEIGHT/2 -105
        self.glitter.set_texture(0)

        # Our starting room number
        self.current_room = self.start_screen

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

        # Draw dirt
        left_dirt = self.rooms[self.current_room].dirt_left_list
        right_dirt = self.rooms[self.current_room].dirt_right_list
        center_dirt = self.rooms[self.current_room].dirt_center_list

        left_dirt.draw()
        right_dirt.draw()
        center_dirt.draw()

        if self.current_room >= self.level1:
            if not left_dirt and not right_dirt and not center_dirt:
                self.glitter.draw()
            self.player.draw()
            # Calculate minutes
            minutes = int(self.total_time) // 60

            # Calculate seconds by using a modulus (remainder)
            seconds = int(self.total_time) % 60

            # Figure out our output
            output = f"Time: {minutes:02d}:{seconds:02d}"

            # Output the timer text.
            arcade.draw_text(output, 50, SCREEN_HEIGHT-50, arcade.color.WHITE, 30)




        """# Draw logo
        if self.current_room==start_screen:
            logo = self.rooms[start_screen].logo
            logo.draw()"""



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.SPACE:
            if self.start_intro:
                self.start_intro = False
            else:
                self.start_intro = True

        if self.start_game:
            if key == arcade.key.UP:
                self.reset_timer('left')
                self.reset_timer('right')
                self.reset_timer('center')

                if self.current_room == start_screen:
                    self.current_room = self.level1
                else:
                    self.current_room = start_screen
            if key == arcade.key.DOWN:
                self.player.center_x = self.position_center_x
                self.player.center_y = self.position_center_y
                if self.current_room == self.level1 or self.current_room == self.level4:
                    self.texture_choice = 16
                else:
                    self.texture_choice = 11

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
        remove_dirt_frame = 2#100//DIRT_COUNT #About 10s total

        timers = [self.left_timer, self.center_timer, self.right_timer]
        lists = [self.rooms[self.current_room].dirt_left_list, self.rooms[self.current_room].dirt_center_list, self.rooms[self.current_room].dirt_right_list]
        for x in range(len(timers)):
            if lists[x]:
                if timers[x] == remove_dirt_frame:
                    self.reset_timer(direction)
                    lists[x][0].alpha -= 5
                    if lists[x][0].alpha < 5:
                        lists[x][0].kill()

    def on_acc_change(self):
        self.arduino_data = arduino.set_Arduino_data()
        x_gyr = self.arduino_data.gyr[0]
        y_gyr = self.arduino_data.gyr[1]
        z_gyr = self.arduino_data.gyr[2]

        x_acc = self.arduino_data.acc[0]
        y_acc = self.arduino_data.acc[1]
        z_acc = self.arduino_data.acc[2]

        self.force = self.arduino_data.force


        #print(force)
        #print("x:")
        #print(x_gyr)
        #print("y:")
        #print(y_gyr)
        #print("z:")
        #print(z_gyr)

        shake = (x_gyr + y_gyr + z_gyr)//3
        self.shake_value_list.append(shake)
        if len(self.shake_value_list) > 20:
            self.shake_value_list.pop(0)
        self.shake_value = statistics.mean(self.shake_value_list)

        self.acc_Y_list.append(y_acc)
        if len(self.acc_Y_list) > 15:
            self.acc_Y_list.pop(0)
        acc_Y_avg = statistics.mean(self.acc_Y_list)
        #print(acc_Y_avg)

        """if not self.acc_X_list:
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
        acc_Z_avg = self.get_avg(self.acc_Z_list)"""

        """Fixed movement"""
        #y-axis -16000 to 16000
        #left = None
        #right = None
        left = self.position_left_x
        right = self.position_right_x
        if test_mode:
            left = self.position_right_x
            right = self.position_left_x

        if acc_Y_avg > 10000 and self.player.center_x != left:
            self.player.center_x = self.position_left_x
            self.texture_choice = 1
            self.player.center_y = self.position_lr_y

        elif -5000 < acc_Y_avg < 5000 and self.player.center_x != self.position_center_x:
            self.player.center_x = self.position_center_x
            self.player.center_y = self.position_center_y
            if self.current_room == self.level1 or self.current_room == self.level4:
                self.texture_choice = 16
            else:
                self.texture_choice = 11

        elif acc_Y_avg < -10000 and self.player.center_x != right:
            self.player.center_x = self.position_right_x
            self.texture_choice = 6
            self.player.center_y = self.position_lr_y

        self.player.set_texture(self.texture_choice)

    def animate_glitter(self):
        self.glitter.set_texture(self.glitter_count)
        self.glitter_count += 1
        if self.glitter_count > 1:
            self.glitter_count = 0

    def animate_player(self):
        animation_framerate = 1
        animation_list = [0, animation_framerate, animation_framerate * 2, animation_framerate * 3]
        """for frame in animation_list:
            if self.frame_timer == frame:"""
        if self.texture_choice == 15:
            self.texture_choice = 16

        self.player.set_texture(self.texture_choice + self.frame_timer)

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
            self.reset_timer('left')
            self.reset_timer('right')
            self.reset_timer('center')

            if next_level == self.level3:
                self.player.set_texture(1)
                self.player.change_x = speed
                self.player.change_y = 0
            else:
                self.player.change_x = 0
                self.player.change_y = speed

            if next_level == 0:
                pygame.mixer.music.pause()
                self.playing_song = False

            if self.player.center_y < - 135 or self.player.center_y > SCREEN_HEIGHT + 135 or self.player.center_x > SCREEN_WIDTH + 150:
                self.current_room = next_level

            elif self.current_room == self.level4 and self.player.center_y > SCREEN_HEIGHT + 120:
                self.current_room = next_level


    def check_if_change_level(self):
        speed = 4
        if self.current_room == self.level1:
            self.switch_level(self.level2, -speed)

        elif self.current_room == self.level2:
            if not self.start_game:
                if self.player.center_x < self.position_center_x -3:
                    self.player.change_x = speed
                elif self.player.center_x > self.position_center_x +3:
                    self.player.change_x = -speed
                else:
                    self.player.change_x = 0

                if self.player.center_y < - 135:
                    self.player.center_y = SCREEN_HEIGHT + 135
                    #self.player.change_y = -8

                if self.player.center_y < self.position_lr_y:
                    self.player.change_y = 0

                if self.player.change_x == 0 and self.player.change_y == 0:
                    center_y = self.position_center_y
                    lr_y = self.position_lr_y
                    self.position_center_y = lr_y
                    self.position_lr_y = center_y
                    self.start_game = True

            self.switch_level(self.level3, speed)

        elif self.current_room == self.level3:
            if not self.start_game:

                if self.player.center_x > SCREEN_WIDTH + 135:
                    self.player.center_x = -135
                    #self.player.change_y = speed

                elif self.player.center_x > self.position_left_x: #self.position_center_x:
                    self.player.change_x = 0

                elif self.player.center_y > self.position_center_y:
                    self.player.change_y = 0

                if self.player.change_x == 0 and self.player.change_y == 0:
                    self.position_center_y = 460
                    self.position_lr_y = 120
                    self.start_game = True

            self.switch_level(self.level4, speed)

        elif self.current_room == self.level4:

            if not self.start_game:
                if self.player.center_x < self.position_center_x -3:
                    self.player.change_x = speed
                elif self.player.center_x > self.position_center_x +3:
                    self.player.change_x = -speed
                else:
                    self.player.change_x = 0

                if self.player.center_y > SCREEN_HEIGHT + 135:
                    self.player.center_y = -135

                elif self.player.center_y > self.position_lr_y:
                    self.player.change_y = 0

                if self.player.change_x == 0 and self.player.change_y == 0:
                    center_y = self.position_center_y
                    lr_y = self.position_lr_y
                    self.position_center_y = lr_y
                    self.position_lr_y = center_y
                    self.start_game = True
            self.switch_level(self.done, speed)

    def update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()

        self.player_list.update()

        force = -1

        if self.current_room == self.done:
            time.sleep(3)
            self.setup()
            self.total_time = 0

        if self.start_game:
            if not self.playing_song:
                pygame.mixer.music.unpause()
                self.playing_song = True

            if self.current_room == self.start_screen:
                self.current_room = self.level1

            self.total_time += delta_time

            if use_arduino:
                self.on_acc_change()
                force = 100
            if self.force > force and not 330 < self.shake_value < 370:
                self.animate_player()

                if self.player.center_x == self.position_left_x:
                    self.remove_dirt('left')
                elif self.player.center_x == self.position_right_x:
                    self.remove_dirt('right')
                else:
                    self.remove_dirt('center')
            else:
                self.player.change_y = 0
                if self.player.center_x == self.position_left_x:
                    self.player.set_texture(0)
                elif self.player.center_x == self.position_right_x:
                    self.player.set_texture(5)
                else:
                    self.player.set_texture(15)

        if self.start_intro:
            self.start_game = False
            if self.current_room == self.start_screen:
                self.current_room = self.intro1
            elif self.current_room == self.intro1:
                self.current_room = self.intro2
                time.sleep(3)
            elif self.current_room == self.intro2:
                self.current_room = self.intro3
                time.sleep(1)
            elif self.current_room == self.intro3:
                self.current_room = self.intro4
                time.sleep(1)
            elif self.current_room == self.intro4:
                self.current_room = self.intro5
                time.sleep(1)
            elif self.current_room == self.intro5:
                self.current_room = self.level1
                self.start_game = True
                self.start_intro = False
                time.sleep(1)
        else:
            self.animate_glitter()
            self.check_if_change_level()





def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
