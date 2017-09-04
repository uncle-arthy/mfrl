#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'

import tdl
#from mfrlHelpers import GameObject

# actual size of the window
SCREEN_WIDTH = 90
SCREEN_HEIGHT = 60

# size of map
MAP_WIDTH = 57
MAP_HEIGHT = 57

color_dark_wall = (51, 41, 26)
color_dark_floor = (26, 20, 13)

LIMIT_FPS = 20  # 20 frames-per-second maximum


class Rect:
    # rectangle on the map to use for rooms
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # block sight if blocked by default
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight


class GameObject:
    # Generic dsplay object
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self. color = color

    def move(self, dx, dy):
        if not my_map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        con.draw_char(self.x, self.y, self.char, self.color, bg=color_dark_floor)

    def clear(self):
        con.draw_char(self.x, self.y, ' ', self.color, bg=color_dark_floor)


def create_room(room):
    global my_map

    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            my_map[x][y].blocked = False
            my_map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
    global my_map
    for x in range(min(x1, x2), max(x1, x2)+1):
        my_map[x][y].blocked = False
        my_map[x][y].block_sight = False


def make_map():
    global my_map

    my_map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(40, 15, 10, 15)
    create_room(room1)
    create_room(room2)

    create_h_tunnel(25, 45, 23)

    player.x = 25
    player.y = 23


def render_all():
    for obj in objects:
        obj.draw()

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = my_map[x][y].block_sight
            if wall:
                con.draw_char(x, y, '#', fg=color_dark_wall, bg=color_dark_floor)
            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_floor)


def handle_keys():
    # turn-based (because "key_wait", well, waits for user input
    user_input = tdl.event.key_wait()

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return True  # exit game

    # movement keys
    if user_input.key == 'UP':
        player.move(0, -1)

    elif user_input.key == 'DOWN':
        player.move(0, 1)

    elif user_input.key == 'LEFT':
        player.move(-1, 0)

    elif user_input.key == 'RIGHT':
        player.move(1, 0)


#############################################
# Initialization & Main Loop                #
#############################################

tdl.set_font('cp437_12x12.png', greyscale=True, altLayout=False)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="MFRL", fullscreen=False)
con = tdl.init(MAP_WIDTH, MAP_HEIGHT)
tdl.setFPS(LIMIT_FPS)

player = GameObject(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', (128, 102, 64))
npc = GameObject(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, '@', (255, 255, 0))
objects = [player, npc]
make_map()


while not tdl.event.is_window_closed():

    render_all()

    root.blit(con, 5, 5, MAP_WIDTH, MAP_HEIGHT, 0, 0)

    tdl.flush()

    for obj in objects:
        obj.clear()

    # handle keys and exit game if needed
    exit_game = handle_keys()
    if exit_game:
        break
