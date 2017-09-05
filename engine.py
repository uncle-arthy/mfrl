#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'Alexei Evdokimov'
'''
Change tutorial from RogueBasin to rogueliketutorials.com
More Pythonic style and seems more OOP-ish ))
'''

import tdl

from entity import Entity
from input_handlers import handle_keys
from map_utils import make_map
from render_functions import clear_all, render_all


def main():
    # set main game window size
    screen_width = 80
    screen_height = 60
    map_width = 80
    map_height = 55

    colors = {
        'dark_wall': (26, 20, 13),
        'dark_ground': (51, 41, 26)
    }

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (128, 102, 64))
    npc = Entity(int(screen_width / 2) - 5, int(screen_height / 2), '@', (255, 255, 0))
    entities = [player, npc]

    # Font differs from one in tutorial as I use this ti work in REXpaint
    tdl.set_font('cp437_12x12.png', greyscale=True, altLayout=False)

    # Main game window
    root_console = tdl.init(screen_width, screen_height, title='MFRL revised tutorial')
    con = tdl.Console(screen_width, screen_height)

    game_map = tdl.map.Map(map_width, map_height)
    make_map(game_map)

    while not tdl.event.is_window_closed():
        render_all(con, entities, game_map, root_console, screen_width, screen_height, colors)

        # And draw it all
        tdl.flush()

        clear_all(con, entities)

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None
        '''
        As in tutorial:
        Python has a lesser-known feature where you can put an 'else' statement
        after a for loop, and that else statement only executes
        if we didn't break out of the loop!
        So in this scenario, if we didn't encounter any 'KEYDOWN' event,
        then we set user_input to None by default.
        '''

        if not user_input:
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if game_map.walkable[player.x + dx, player.y + dy]:
                player.move(dx, dy)

        if exit_game:
            return True  # Exit main loop and the game

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())


if __name__ == '__main__':
    main()